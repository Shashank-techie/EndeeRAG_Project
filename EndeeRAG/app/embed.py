from sentence_transformers import SentenceTransformer
from typing import List
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def generate_embeddings(texts: List[str]):
    embeddings = model.encode(texts)
    return embeddings.tolist()  # convert numpy array → Python list
