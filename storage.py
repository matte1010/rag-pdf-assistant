import faiss
import pickle

def save_index(index, chunks):
    faiss.write_index(index, "index.faiss")
    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_index():
    index = faiss.read_index("index.faiss")
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks