from qdrant_client import QdrantClient
from config import HOSTNAME, QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import torch

qdrand_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
mongo_client = MongoClient(f'mongodb://{HOSTNAME}:{27017}').get_database('scientific_articles')

qdrant_papers = qdrand_client.get_collection(collection_name="papers")
mongo_articles = mongo_client.get_collection('articles')

transformer = SentenceTransformer(
  "msmarco-MiniLM-L-6-v3",
  device="cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"),
)
transformer = transformer.eval()