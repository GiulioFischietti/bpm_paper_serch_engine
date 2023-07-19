import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse, SummaryBody
from access_points import QdrantQueryThread, mongo_articles, encoder
from logic import weighted_query
from config import OPENAI_API_KEY, OPENAI_FREE_URL, ALLOWED_ORIGINS
from openai import ChatCompletion
from torch import squeeze
import threading
import json
import requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=["*"])

@app.get("/search")
def get_search(query: str, page: int):

  links = weighted_query(query=query, page=page)

  parsings = mongo_articles.find({
    "link":{
      "$in": links
    }
  })

  final_response = [SearchResponse(
    doc["title"], 
    doc["publication_date"], 
    doc["summary"], 
    doc["link"], 
    doc["authors"]
  ) for doc in parsings if "summary" in doc]

  return JSONResponse(jsonable_encoder(ErrorScheme("frek't", HTTPStatus.BAD_REQUEST))) if query == ""\
    else JSONResponse(jsonable_encoder(final_response))

@app.put("/summary")
def get_summary(body: SummaryBody):
  links = body.links
  query = body.query

  parsings = mongo_articles.find({
    "link":{
      "$in": links
    }
  })
  results = list(parsings)

  '''
  You have been asked: AI in modern society by a phd. Provide a 800-1000 word article with an Introduction, a Discussion and some final Conclusions and return it in json format with each section and its content. Build the article from the following sciencedirect papers:
  0. https://www.sciencedirect.com/science/article/pii/S0040162523002640
  1. https://www.sciencedirect.com/science/article/pii/S0160791X22003153
  2. https://www.sciencedirect.com/science/article/pii/S138650562300059X
  Reference the articles parts with [0] where 0 is the index relative to the article and give a title to the article.
  '''

  prompt = f'You have been asked: "{query}" by a phd. Provide a 800-1000 word article with a Title, an Introduction, \
    a Discussion and some final Conclusions and return it in json format following the pattern "section":"content". \
    Also include the information given by the following paper\'s summaries:\n' 
  for idx, doc in enumerate(results):
    prompt += f'index: {idx}; title: {doc["title"]}; summary: {doc["summary"]} link: {doc["link"]}\n'
    continue
  prompt += f'Reference the papers with [index] where index is the one relative to the paper you are mentioning.'
  
  '''
    answer = openaiRequest(prompt)
  '''

  print(prompt)

  answer = json.loads('''{
  "Introduction": "Artificial Intelligence (AI) has become an integral part of modern society, revolutionizing various sectors and transforming the way we live and work. This article explores the impact of AI on society, focusing on its economic effects, research trends, and potential applications. Drawing insights from recent studies, including [0], [1], and [2], we delve into the key aspects of AI's influence in different domains.",
  "Discussion": "The economic effects of AI have been extensively discussed in previous research, highlighting how digital technologies like AI and big data disrupt business models, enhance productivity, reduce waste, and improve stakeholder experiences. Studies have shown that AI adoption and the utilization of big data analytics have a significant impact on industries such as manufacturing, as observed in South Africa's automobile sector [0]. By leveraging big data, businesses can gain valuable insights and make data-driven decisions efficiently and effectively. Furthermore, AI's potential for technology roadmapping, patent mining, and breakthrough identification has received substantial attention, constituting a notable research theme [0]. This indicates the importance of exploring AI's role in shaping technological advancements and identifying opportunities for future growth.\n\nThe field of robotics is closely intertwined with AI and has made significant contributions to society. Various categories of robotics, such as industrial robotics, service robotics, and social robotics, have emerged as key research areas. Studies have examined fundamental aspects of robotics, including human values and expectations, as well as broader issues like the relationship between employment and productivity [1]. Service robots, specifically in the hospitality industry, have been studied to understand their impact on customer experiences and operational efficiency [1]. Such research sheds light on the social implications and ethical considerations associated with integrating robotics into society.\n\nAI's impact extends beyond the realm of robotics and into healthcare. In the context of cardiovascular disease, AI has been explored for secondary prevention of myocardial infarction (MI). By leveraging AI-enabled systems, tailored feedback and general advice can be provided to patients, aiding in the management of their conditions [2]. However, concerns regarding privacy and the ethical use of AI in healthcare settings have been raised. Transparency and explainability in AI systems play a crucial role in establishing trust among patients and healthcare professionals [2]. Understanding patient and health professional perspectives is vital for the successful implementation and acceptance of AI in healthcare.\n\nThe evolution of AI research in recent years reveals significant advancements and emerging trends. Researchers have identified key topics in AI, which have evolved over time and continue to shape the field. These topics include technology roadmapping, big data analytics, industrial robotics, and adoption of AI-enabled systems [0, 1]. Future research endeavors should focus on exploring these topics further, understanding their conceptual structure, and bridging interdisciplinary gaps to foster collaboration and innovation.\n\nOverall, AI's integration into modern society has profound implications. It drives economic growth, enhances operational efficiency, and transforms various sectors such as manufacturing, hospitality, and healthcare. However, ethical considerations, transparency, and trust-building are crucial factors that need to be addressed for responsible and successful AI implementation. By considering these aspects, society can harness the full potential of AI while ensuring its benefits are widely accessible and equitable.",
  "Conclusions": "Artificial Intelligence has become an indispensable part of modern society, revolutionizing multiple domains and bringing forth significant economic, social, and technological transformations. The economic impact of AI is evident in its ability to disrupt traditional business models, boost productivity, and provide enhanced stakeholder experiences. Big data analytics and AI-driven insights have proven instrumental in decision-making processes, particularly in industries such as manufacturing. The research trends in AI have focused on key areas like technology roadmapping, big data analytics, and industrial robotics, demonstrating the importance of interdisciplinary collaboration. Robotics, closely intertwined with AI, has explored fundamental human values, employment dynamics, and the integration of service robots in sectors like hospitality. In healthcare, AI has shown promise in secondary prevention of myocardial infarction, emphasizing the need for transparent and trustworthy AI systems. Moving forward, it is essential to address ethical considerations and establish trust to ensure responsible AI implementation and maximize its benefits for society.",
  "Title": "The Impact of Artificial Intelligence on Modern Society"
  }''', strict=False)
  
  section_text = f'<h1 style="text-align:center;">{answer["Title"] if "Title" in answer else "Mannaggia a ChatGPT"}</h1>'
  empty_stack = True
  for section in answer:
    empty_stack = False
    if section == "Title":
      continue
    section_text += f'<h2>{section.upper()}</h2>'
    section_text += f'<p>{answer[section]}'
  
  section_text += "<h2>REFERENCES</h2>"
  for idx, doc in enumerate(results):
    section_text += f'<p>[{idx}]\t<a href={doc["link"]} target="_blank">{doc["title"]}</a></p>'    

  return section_text if not empty_stack else jsonable_encoder(ErrorScheme("No results found, the issue may be caused by an unwanted page reload, reloading the page in this stage of the application may cause a wrong format for the request", HTTPStatus.BAD_REQUEST))