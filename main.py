from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_pipeline import build_vector_store, ask_llm
from src.classifier import(
    detect_priority,
    detect_category,
    detect_sentiment,
    escalation_needed
)

app = FastAPI(title="AI Support Copilot")

build_vector_store()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
   return {"message": "AI Support Copilot Running"}


@app.post("/ask")
def ask_question(data: QueryRequest):
    try:
        answer = ask_llm(data.query)

        priority = detect_priority(data.query)
        category = detect_category(data.query)
        sentiment = detect_sentiment(data.query)
        escalation = escalation_needed(priority, sentiment)

        return {
            "query": data.query,
            "answer": answer,
            "priority": priority,
            "category": category,
            "sentiment": sentiment,
            "escalation": escalation
        }

    except Exception as e:
        return {"error": str(e)}




