from .search import semantic_search
import google.genai as genai
import os

# Configure Google Gemini API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyAF1--d0-DDorel0h0JTVlYuV0lFVD_rzk"))

def generate_answer(query):
    context_chunks = semantic_search(query)
    context = "\n".join(context_chunks)

    prompt = f"""
    Use the following context to answer the question:

    Context:
    {context}

    Question: {query}
    Answer:
    """

    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )

    return response.text
