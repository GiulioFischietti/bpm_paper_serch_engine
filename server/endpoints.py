import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse
from access_points import qdrand_client, mongo_articles, transformer
from config import OPENAI_API_KEY, OPENAI_FREE_URL, ALLOWED_ORIGINS
from openai import ChatCompletion
import json
import requests


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS)

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
def get_summary(links:list[str]):
  parsings = mongo_articles.find({
    "link":{
      "$in": links
    }
  })

  # TODO: request to openAI for the response
  '''
    prompt = "You have been asked: " + query +  " by a phd. Provide a  800-1000 word answer with title, introduction, discussion and conclusions considering the following pieces of articles found on sciencedirect, considering that some of them may belong to the same article or be of the same topic and mentioning them if necessary like this: [0], [1] and so on:\n" 
    for idx, doc in enumerate(parsings):
      prompt += f'{idx}. title: "{doc["title"]}" {doc["abstract"]}\n'
      continue
  '''
  
  section_text = ""
  emptyStack = True
  for section in ["introduction", "discussion", "conclusions"]:
    section_text = f"<h2>{section.upper()}<h2>"
    section_text+="<p>"
    for idx, doc in enumerate(parsings):
      emptyStack = False
      if section == "introduction" and idx == 0:
        section_text = f'<h1>{doc["title"]}</h1>'
      section_text += doc["abstract"][:30] if section == "introduction" else\
        doc["body"][:100] if section == "discussion" else doc["conclusions"][:30]
      section_text += f'<a href={doc["link"]}>[{idx}]</a>'
    section_text+="</p>"

  return section_text if not emptyStack else jsonable_encoder(ErrorScheme("frek't", HTTPStatus.BAD_REQUEST))