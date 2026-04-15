from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from contextlib import asynccontextmanager
import shutil
import os

from ingest import load_pdf, chunk_text
from rag import build_index, search
from llm import answer
from storage import save_index, load_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    global index, chunks
    try:
        index, chunks = load_index()
        print("Loaded existing index from disk")
    except:
        print("No existing index found")
        index, chunks = None, None

    yield  # app runs here


app = FastAPI(lifespan=lifespan)

# Global state
index = None
chunks = None

# Upload PDF
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    global index, chunks

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)
    chunks = chunk_text(text)
    index = build_index(chunks)

    save_index(index, chunks)

    return {"message": "PDF uploaded and indexed successfully"}


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    global index, chunks

    if index is None or chunks is None:
        return {"error": "No PDF uploaded yet"}

    retrieved = search(query.question, index, chunks)
    response = answer(query.question, retrieved)

    return {
        "question": query.question,
        "answer": response,
        "sources": [int(r["source"]) for r in retrieved]
    }