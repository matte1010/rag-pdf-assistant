from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    i = 0

    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += chunk_size - overlap

    return chunks