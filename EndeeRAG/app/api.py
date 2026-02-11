from fastapi import FastAPI
from .rag import generate_answer

app = FastAPI()

@app.get("/query")
def query(q: str):
    return {"answer": generate_answer(q)}
