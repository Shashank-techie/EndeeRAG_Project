#!/usr/bin/env python3
"""
Simple terminal script to query the EndeeRAG API
Usage: python query_terminal.py "Your question here"
"""

import sys
import requests
import json

def query_api(question):
    url = "http://127.0.0.1:8000/query"
    headers = {"Content-Type": "application/json"}
    data = {"q": question}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            print(f"🤖 Answer: {result['answer']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python query_terminal.py \"Your question here\"")
        sys.exit(1)

    question = sys.argv[1]
    print(f"🔍 Query: {question}")
    query_api(question)
