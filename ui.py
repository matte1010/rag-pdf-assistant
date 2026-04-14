import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📄 RAG PDF Assistant")

# -----------------------
# Upload section
# -----------------------
st.header("1. Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.button("Upload"):
        files = {"file": uploaded_file.getvalue()}

        response = requests.post(
            f"{API_URL}/upload",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            st.success("PDF uploaded successfully!")
        else:
            st.error("Upload failed")

# -----------------------
# Question section
# -----------------------
st.header("2. Ask questions")

question = st.text_input("Your question")

if st.button("Ask") and question:
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    if response.status_code == 200:
        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Sources")
        st.write(data["sources"])