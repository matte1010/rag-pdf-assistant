from ingest import load_pdf, chunk_text
from rag import build_index, search
from llm import answer

def run_cli():
    text = load_pdf("data/test.pdf")
    chunks = chunk_text(text)
    index = build_index(chunks)

    print("CLI RAG ready (type 'exit' to quit)\n")

    while True:
        query = input("Ask a question: ")

        if query.lower() in ["exit", "quit"]:
            break

        retrieved = search(query, index, chunks)
        response = answer(query, retrieved)

        print("\nAnswer:\n", response)
        print("\nSources:", [r["source"] for r in retrieved])
        print("-" * 40)


if __name__ == "__main__":
    run_cli()