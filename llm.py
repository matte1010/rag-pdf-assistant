import ollama


def answer(query, retrieved_chunks):
    context = "\n\n".join(
        [f"[Source {c['source']}]: {c['text']}" for c in retrieved_chunks]
    )

    prompt = f"""
You are a precise assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Return a clear and structured answer.
Include sources (Source X) when relevant.
"""

    res = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]