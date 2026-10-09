import os
import fitz
import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

PRIMARY_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

FALLBACK_MODEL = os.getenv(
    "GROQ_FALLBACK_MODEL",
    "openai/gpt-oss-20b"
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
index = None


def extract_text_from_pdfs(folder="data/docs"):
    text = ""

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            pdf = fitz.open(os.path.join(folder, file))
            for page in pdf:
                text += page.get_text() + "\n"

    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def build_vector_store():
    global documents, index

    raw_text = extract_text_from_pdfs()
    documents = chunk_text(raw_text)

    embeddings = embedding_model.encode(documents)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))


def retrieve_context(query):
    global documents, index

    q = embedding_model.encode([query])

    distances, indices = index.search(np.array(q), k=3)

    results = [documents[i] for i in indices[0]]

    return "\n\n".join(results)


def ask_llm(query):
    context = retrieve_context(query)

    prompt = f"""
You are a professional Blinkit customer support assistant.

Use the context below to answer clearly and politely.

Context:
{context}

Customer Query:
{query}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:

        if getattr(e, "status_code", None) == 404:

            print(
                f"Primary model '{PRIMARY_MODEL}' is unavailable. "
                f"Trying fallback model '{FALLBACK_MODEL}'."
            )

            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content

        raise