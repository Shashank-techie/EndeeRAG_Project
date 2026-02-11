#!/usr/bin/env python3
"""
Demo script for EndeeRAG RAG System
Run this from the EndeeRAG directory: python demo_queries.py
"""

from app.query import RAGQueryEngine

def run_demo_queries():
    print("🚀 Running EndeeRAG Demo Queries...")

    # Initialize the RAG query engine
    engine = RAGQueryEngine()

    # Sample queries based on the sample FAQ data
    demo_queries = [
        "What is the refund policy?",
        "How can I reset my password?",
        "What is the onboarding process for new employees?",
        "Can customers get refunds after 30 days?",
        "How do users reset their passwords?"
    ]

    print(f"📋 Running {len(demo_queries)} demo queries...\n")

    for i, query in enumerate(demo_queries, 1):
        print(f"🔍 Query {i}: {query}")
        try:
            answer = engine.ask(query)
            print(f"🤖 Answer: {answer}\n")
        except Exception as e:
            print(f"❌ Error processing query: {e}\n")

    print("✅ Demo completed!")

if __name__ == "__main__":
    run_demo_queries()
