import streamlit as st
import requests

st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Blinkit AI Support Copilot")

st.write("Ask questions about refunds, shipping, orders, cancellations.")

query = st.text_input("Enter your question:")

if st.button("Ask"):

    if query.strip():
 
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"query": query}
            )

            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.success(data["answer"])

            st.subheader("Answer:")
            

            st.write("### Priority :", data["priority"])
            st.write("### Category :", data["category"])
            st.write("### Sentiment :", data["sentiment"])
            
            st.write("### Escalation Needed :", data["escalation"])
            
            