# pylint: disable=no-name-in-module
from pydantic import BaseModel
from dataclasses import dataclass, asdict

@dataclass(init=True)
class SearchResponse():
  '''
    title got from chatGPT, body represents the content of the genrated response, conclusions is a brief summary of the content
    sources is a list of link to the references from which the answer has been generated
  '''
  title: str
  body: str
  conclutions: str
  sources: list[str]

  def dict(self):
    return {k: str(v) for k,v in asdict(self).items()}


@dataclass(init=True)
class ErrorScheme():
  message: str
  code: int
  
  def dict(self):
    return {k: str(v) for k,v in asdict(self).items()}