import streamlit as st
import requests

st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="🤖",
    layout="wide"
)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.write("### About")
    st.write("AI-powered customer support assistant using RAG + LLM.")

# Main Title
st.title("🤖 Blinkit AI Support Copilot")
st.caption("Ask about refunds, shipping, delivery, cancellations.")

# Input
query = st.text_input("Enter your question:")

if st.button("Ask"):

    if query.strip():

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"query": query}
        )

        data = response.json()

        st.session_state.messages.append(
            {
                "query": query,
                "answer": data["answer"],
                "priority": data["priority"],
                "category": data["category"],
                "sentiment": data["sentiment"],
                "escalation": data["escalation"]
            }
        )

# Chat History
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