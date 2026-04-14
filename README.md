# RAG PDF Assistant

A Retrieval-Augmented Generation (RAG) system for asking questions over PDF documents using semantic search and a local LLM.

The system combines FastAPI, FAISS vector search, and Ollama (Llama 3) for retrieval-based question answering, with a Streamlit UI for interaction.

---

## 🚀 Features

- Upload PDF documents dynamically
- Semantic search using embeddings (FAISS)
- Local LLM inference via Ollama (Llama 3)
- FastAPI backend for scalable API design
- Streamlit frontend for simple user interaction
- Source tracking from retrieved chunks

---

## 🧠 Architecture

1. PDF is uploaded via UI
2. Text is extracted and split into chunks
3. Embeddings are generated for each chunk
4. FAISS index is built for similarity search
5. User question is embedded and matched to relevant chunks
6. Retrieved context is sent to LLM (Ollama)
7. Final answer is returned via API

---

## 🛠 Tech Stack

- Python
- FastAPI
- Streamlit
- FAISS
- SentenceTransformers
- Ollama (Llama 3)
- PyPDF / PDF parsing tools

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/rag-pdf-assistant.git
cd rag-pdf-assistant

python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt