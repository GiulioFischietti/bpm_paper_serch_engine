import os
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from http import HTTPStatus
from schemes import ErrorScheme, SearchResponse

app = FastAPI()

@app.get("/search")
def get_search(query: str):
  return JSONResponse(jsonable_encoder(ErrorScheme("frek't", HTTPStatus.BAD_REQUEST))) if query == ""\
    else JSONResponse(jsonable_encoder(SearchResponse(title="", body="", conclutions="", sources=[])))


