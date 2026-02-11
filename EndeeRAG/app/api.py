from fastapi import FastAPI
from pydantic import BaseModel
from .rag import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    q: str

@app.post("/query")
def query(request: QueryRequest):
    return {"answer": generate_answer(request.q)}
