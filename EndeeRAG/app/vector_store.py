import requests
from typing import List
import msgpack
import json
import os
from config import ENDEE_INDEX_PATH, EMBEDDING_MODEL

ENDEE_URL = "http://127.0.0.1:8080"
INDEX_NAME = "rag_index"
VECTOR_DIM = 384
TEXTS_FILE = "endee_texts.json"


class EndeeVectorStore:
    def __init__(self):
        self.base_url = ENDEE_URL
        self.texts = {}  # id -> text mapping
        self._load_texts()
        self._ensure_index()

    def _ensure_index(self):
        url = f"{self.base_url}/api/v1/index/list"
        res = requests.get(url).json()

        index_names = [idx["name"] for idx in res.get("indexes", [])]

        if INDEX_NAME not in index_names:
            print(f"⚙️ Creating index: {INDEX_NAME}")
            create_url = f"{self.base_url}/api/v1/index/create"
            payload = {
                "index_name": INDEX_NAME,
                "dim": VECTOR_DIM,
                "space_type": "cosine"
            }
            r = requests.post(create_url, json=payload)
            print("🧾 Create index response:", r.text)
        else:
            print(f"✅ Index exists: {INDEX_NAME}")
            # If index exists but we have no texts, we need to re-ingest
            if not self.texts:
                self._reingest_documents()

    def add_documents(self, texts: List[str], embeddings: List[List[float]]):
        url = f"{self.base_url}/api/v1/index/{INDEX_NAME}/vector/insert"

        vectors = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            vector_id = str(i)
            vectors.append({
                "id": vector_id,
                "vector": emb
            })
            self.texts[vector_id] = text  # Store text for retrieval

        payload = vectors

        r = requests.post(url, json=payload)
        print("💾 Insert response:", r.text)
        self._save_texts()  # Persist texts after insertion

    def search(self, query_embedding: List[float], top_k: int = 5):
        url = f"{self.base_url}/api/v1/index/{INDEX_NAME}/search"

        payload = {
            "vector": query_embedding,
            "k": top_k
        }

        r = requests.post(url, json=payload)
        raw_results = msgpack.unpackb(r.content)

        print(f"🔍 Raw search results: {raw_results}")  # Debug print

        # Convert to expected format with texts
        results = []
        if isinstance(raw_results, list):
            # Format: [[distance, id, metadata, text, score, extra], ...]
            for item in raw_results:
                if len(item) >= 2:
                    distance = item[0]
                    vector_id = str(item[1])
                    # Always use stored text since server doesn't store text
                    text = self.texts.get(vector_id, "")
                    results.append({
                        "id": vector_id,
                        "text": text,
                        "distance": distance
                    })

        return {"results": results}

    def _reingest_documents(self):
        """Re-ingest documents when index exists but texts are missing"""
        try:
            from .ingest import prepare_chunks
            from .embed import generate_embeddings

            print("🔄 Re-ingesting documents...")
            chunks = prepare_chunks()
            embeddings = generate_embeddings(chunks)
            self.add_documents(chunks, embeddings)
            print("✅ Documents re-ingested successfully")
        except Exception as e:
            print(f"❌ Failed to re-ingest documents: {e}")

    def _load_texts(self):
        """Load persisted texts from file"""
        if os.path.exists(TEXTS_FILE):
            with open(TEXTS_FILE, 'r') as f:
                self.texts = json.load(f)

    def _save_texts(self):
        """Save texts to file for persistence"""
        with open(TEXTS_FILE, 'w') as f:
            json.dump(self.texts, f)


# ---------- CLI TEST ----------
if __name__ == "__main__":
    from .ingest import prepare_chunks
    from .embed import generate_embeddings

    print("📥 Loading documents...")
    chunks = prepare_chunks()

    print("🧠 Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    print("💾 Storing vectors in Endee...")
    store = EndeeVectorStore()
    store.add_documents(chunks, embeddings)

    print("✅ Endee index created successfully!")
