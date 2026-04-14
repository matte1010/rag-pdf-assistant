from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from ingest import load_pdf, chunk_text
from rag import build_index, search
from llm import answer

app = FastAPI()

# In-memory storage (simple version)
chunks = None
index = None


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    global chunks, index

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)
    chunks = chunk_text(text)
    index = build_index(chunks)

    return {"message": "PDF uploaded and indexed successfully"}


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    if index is None:
        return {"error": "No PDF uploaded yet"}

    retrieved = search(query.question, index, chunks)
    response = answer(query.question, retrieved)

    return {
        "question": query.question,
        "answer": response,
        "sources": [int(r["source"]) for r in retrieved]
    }