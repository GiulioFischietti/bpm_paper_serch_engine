import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse
from access_points import qdrand_client, mongo_articles, transformer
from config import OPENAI_API_KEY, OPENAI_FREE_URL
from openai import ChatCompletion
import requests


app = FastAPI()

@app.get("/search")
def get_search(query: str):
  # from qdrant: link -> get by link from MongoDB ["title", "link", "summary"]
  encoded_query = transformer.encode(query)
  links = qdrand_client.search(collection_name="papers_complete", query_vector=encoded_query, limit=6)
  links = [l.payload["link"] for l in links]

  parsings = mongo_articles.find({
    "link":{
      "$in": links
    }
  })

  prompt = "You have been asked: " + query + " by a phd. Provide a 1000 word answer with introduction, discussion and conclusions considering the following pieces of articles found on sciencedirect, considering that some of them may belong to the same article or be of the same topic and mentioning them if necessary like this: [0], [1] and so on:\n" 
  for idx, doc in enumerate(parsings):
    prompt += f'{idx}. title: "{doc["title"]}" {doc["abstract"]}\n'
    continue
  
  # TODO: request to openAI for the response

  print(openai_response)

  return JSONResponse(jsonable_encoder(ErrorScheme("frek't", HTTPStatus.BAD_REQUEST))) if query == ""\
    else JSONResponse(jsonable_encoder(openai_response))