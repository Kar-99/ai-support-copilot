import streamlit as st
from src.rag_pipeline import build_vector_store, ask_llm
from src.classifier import (
    detect_priority,
    detect_category,
    detect_sentiment,
    escalation_needed
)

st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="🤖",
    layout="wide"
)

# Build vector store once
@st.cache_resource
def initialize():
    build_vector_store()

initialize()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.write("### About")
    st.write("AI-powered customer support assistant using RAG + Groq LLM.")

# Main UI
st.title("🤖 Blinkit AI Support Copilot")
st.caption("Ask about refunds, shipping, delivery, cancellations.")

query = st.text_input("Enter your question:")

if st.button("Ask"):

    if query.strip():

        with st.spinner("Thinking..."):

            answer = ask_llm(query)

            priority = detect_priority(query)
            category = detect_category(query)
            sentiment = detect_sentiment(query)
            escalation = escalation_needed(priority, sentiment)

            st.session_state.messages.append({
                "query": query,
                "answer": answer,
                "priority": priority,
                "category": category,
                "sentiment": sentiment,
                "escalation": escalation
            })

# Chat history
for chat in reversed(st.session_state.messages):

    st.markdown("---")
    st.subheader("👤 User")
    st.info(chat["query"])

    st.subheader("🤖 AI Response")
    st.success(chat["answer"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Priority", chat["priority"])

    with col2:
        st.metric("Category", chat["category"])

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Sentiment", chat["sentiment"])

    with col4:
        st.metric("Escalation", chat["escalation"])