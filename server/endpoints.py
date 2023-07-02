import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse, SummaryBody
from access_points import qdrand_client, mongo_articles, transformer
from config import OPENAI_API_KEY, OPENAI_FREE_URL, ALLOWED_ORIGINS
from openai import ChatCompletion
import json
import requests


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=["*"])

@app.get("/search")
def get_search(query: str, page: int):
  # from qdrant: link -> get by link from MongoDB ["title", "link", "summary"]
  encoded_query = transformer.encode(query)
  links = qdrand_client.search(collection_name="papers_complete", query_vector=encoded_query, limit=6, offset=page*6)
  links = [l.payload["link"] for l in links]

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
  print(body.query)
  parsings = mongo_articles.find({
    "link":{
      "$in": links
    }
  })
  results = list(parsings)

  # TODO: request to openAI for the response
  '''
    prompt = "You have been asked: " + query +  " by a phd. Provide a  800-1000 word answer with title, introduction, discussion and conclusions considering the following pieces of articles found on sciencedirect, considering that some of them may belong to the same article or be of the same topic and mentioning them if necessary like this: [0], [1] and so on:\n" 
    for idx, doc in enumerate(parsings):
      prompt += f'{idx}. title: "{doc["title"]}" {doc["abstract"]}\n'
      continue
  '''
  
  section_text = ""
  empty_stack = True
  for section in ["introduction", "discussion", "conclusions"]:
    section_text += f"<h2>{section.upper()}</h2>"
    section_text +='<p>'
    for idx, doc in enumerate(results):
      empty_stack = False
      if section == "introduction" and idx == 0:
        section_text = f'<h1>{doc["title"]}</h1>'
      section_text += doc["abstract"][:1000] if section == "introduction" else\
        doc["body"][:3000] if section == "discussion" else doc["body"][len(doc["body"])-1001:len(doc["body"])-1001+1000]
      section_text += f'<a href={doc["link"]} target="_blank">[{idx}]</a>'
    section_text+="</p>"
  
  section_text += "<h2>REFERENCES</h2>"
  for idx, doc in enumerate(results):
    section_text += f'<p><a href={doc["link"]}>{doc["title"]}</a></p>'    

  return section_text if not empty_stack else jsonable_encoder(ErrorScheme("No results found, the issue may be caused by an unwanted page reload, reloading the page in this stage of the application may cause a wrong format for the request", HTTPStatus.BAD_REQUEST))