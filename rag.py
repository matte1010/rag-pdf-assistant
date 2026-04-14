import faiss
import numpy as np
import ollama


def embed(text):
    res = ollama.embeddings(
        model="llama3",
        prompt=text
    )
    return np.array(res["embedding"], dtype="float32")


def build_index(chunks):
    vectors = np.array([embed(c) for c in chunks]).astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    return index


def search(query, index, chunks, k=3):
    q_vec = embed(query).reshape(1, -1)

    distances, indices = index.search(q_vec, k)

    results = []
    for i in indices[0]:
        results.append({
            "text": chunks[i],
            "source": int(i)
        })

    return results