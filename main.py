from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_pipeline import build_vector_store, ask_llm

app = FastAPI(title="AI Support Copilot")

build_vector_store()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
   return {"message": "AI Support Copilot Running"}


@app.post("/ask")
def ask_question(data: QueryRequest):
    answer = ask_llm(data.query)

    return {
        "query": data.query,
        "answer": answer
    }