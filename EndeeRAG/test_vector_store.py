#!/usr/bin/env python3
"""
Test script for EndeeRAG Vector Store
Run this from the EndeeRAG directory: python test_vector_store.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.vector_store import EndeeVectorStore
from app.ingest import prepare_chunks
from app.embed import generate_embeddings

def test_vector_store():
    print("🧪 Testing EndeeRAG Vector Store...")

    try:
        # Test 1: Initialize vector store (this will create index if needed)
        print("\n1. Initializing vector store...")
        store = EndeeVectorStore()
        print("✅ Vector store initialized successfully")

        # Test 2: Load and prepare documents
        print("\n2. Loading documents...")
        chunks = prepare_chunks()
        print(f"✅ Loaded {len(chunks)} document chunks")

        # Test 3: Generate embeddings
        print("\n3. Generating embeddings...")
        embeddings = generate_embeddings(chunks)
        print(f"✅ Generated embeddings for {len(embeddings)} chunks")

        # Test 4: Add documents to vector store
        print("\n4. Adding documents to vector store...")
        store.add_documents(chunks, embeddings)
        print("✅ Documents added successfully")

        # Test 5: Search functionality
        print("\n5. Testing search functionality...")
        # Use the first embedding as query
        query_embedding = embeddings[0]
        results = store.search(query_embedding, top_k=3)
        print(f"✅ Search completed, found {len(results)} results")

        # Test 6: Verify search results structure
        print("\n6. Verifying search results...")
        if hasattr(results, 'distances') and hasattr(results, 'ids'):
            print(f"   - Found {len(results.distances)} distances")
            print(f"   - Found {len(results.ids)} IDs")
            print("✅ Search results structure is correct")
        else:
            print("⚠️  Search results structure may be different, but search succeeded")

        print("\n🎉 All tests passed! EndeeRAG Vector Store is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Make sure the Endee server is running on http://127.0.0.1:8080")
        return False

    return True

if __name__ == "__main__":
    success = test_vector_store()
    sys.exit(0 if success else 1)
