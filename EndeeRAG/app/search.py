from .embed import generate_embeddings
from .vector_store import EndeeVectorStore
from config import TOP_K

def semantic_search(query):
    emb = generate_embeddings([query])[0]
    store = EndeeVectorStore()
    results = store.search(emb, top_k=TOP_K)
    return [r["text"] for r in results["results"]]
