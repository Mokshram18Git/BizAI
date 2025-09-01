import requests
from utils import chunk_text

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def get_answer(query, documents):
    context_chunks = []
    sources = []

    for doc in documents:
        chunks = chunk_text(doc["text"], max_words=250)
        context_chunks.extend(chunks)
        sources.append(doc["url"])

    full_context = "\n\n".join(context_chunks[:5])  # More context = better answers

    prompt = f"""
You are a business analyst AI. Based on the context below, do the following:

1. Give a detailed answer to the user query.
2. Extract recent revenue, profit, sales, or growth if available.
3. Give a prediction or business forecast for next year or near future.
4. Be very informative, insightful, and not short.

CONTEXT:
{full_context}

QUESTION:
{query}

ANSWER:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    answer = response.json().get("response", "Sorry, could not answer.")
    return answer.strip(), sources
