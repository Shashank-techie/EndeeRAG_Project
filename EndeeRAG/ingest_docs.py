#!/usr/bin/env python3
"""
Script to ingest documents into the EndeeRAG vector store
"""

from app.ingest import prepare_chunks
from app.embed import generate_embeddings
from app.vector_store import EndeeVectorStore

def ingest_documents():
    print("🚀 Starting document ingestion...")

    # Prepare chunks from documents
    print("📄 Preparing document chunks...")
    chunks = prepare_chunks()
    print(f"📊 Found {len(chunks)} chunks")

    if not chunks:
        print("❌ No documents found to ingest")
        return

    # Generate embeddings
    print("🧠 Generating embeddings...")
    embeddings = generate_embeddings(chunks)
    print(f"🔢 Generated {len(embeddings)} embeddings")

    # Store in Endee vector store
    print("💾 Storing in vector database...")
    store = EndeeVectorStore()
    store.add_documents(chunks, embeddings)
    print("✅ Document ingestion complete!")

if __name__ == "__main__":
    ingest_documents()
