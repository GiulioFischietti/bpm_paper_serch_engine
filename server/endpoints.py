import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse
from access_points import qdrant_papers, mongo_articles

app = FastAPI()

@app.get("/search")
def get_search(query: str):
  # from qdrant: id -> get by id from MongoDB ["title", "link", "summary"]
  
  return JSONResponse(jsonable_encoder(ErrorScheme("frek't", HTTPStatus.BAD_REQUEST))) if query == ""\
    else JSONResponse(jsonable_encoder(SearchResponse(title="", body="", conclutions="", sources=[])))


