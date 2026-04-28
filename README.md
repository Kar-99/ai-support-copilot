# AI Customer Support Copilot

An AI-powered support automation system using RAG and NLP.

## Features
- Ask questions from docs
- Priority detection
- Ticket routing
- Sentiment analysis

![App Screenshot](assets/ss1.png)


## Tech Stack
Python, FastAPI, Streamlit, LangChain, FAISS

## Project Architecture

![App Screenshot](assets/ss3.png)

## Run Locally

pip install -r requirements.txt

uvicorn main:app --reload

streamlit run app.py
![App Screenshot](assets/ss2.png)