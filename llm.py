import ollama


def answer(question, retrieved_chunks):
    # Build context
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"[Source {i}] {chunk['text']}\n\n"

    prompt = f"""
You are a precise and reliable assistant.

Rules:
- Answer ONLY using the provided context.
- Do NOT use outside knowledge.
- If the answer is not in the context, say: "I don't know".
- Always include source references like [Source X].

Context:
{context}

Question:
{question}

Answer:
"""

    import ollama

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]