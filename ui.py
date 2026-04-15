import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Assistant", page_icon="📄", layout="centered")

st.title("📄 Chat with your PDF")
st.caption("Upload a document and ask questions using AI")

# -----------------------
# Upload section
# -----------------------
st.header("1. Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Track state
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "last_file" not in st.session_state:
    st.session_state.last_file = None

if uploaded_file is not None:
    # Reset if new file
    if uploaded_file.name != st.session_state.last_file:
        st.session_state.uploaded = False
        st.session_state.last_file = uploaded_file.name

    if not st.session_state.uploaded:
        with st.spinner("Uploading and indexing..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            st.success(f"Loaded: {uploaded_file.name}")
            st.session_state.uploaded = True
        else:
            st.error(f"Upload failed: {response.text}")

# -----------------------
# Chat section
# -----------------------
st.header("2. Chat with your PDF")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Ask a question about your PDF"):

    if not st.session_state.uploaded:
        st.warning("Please upload a PDF first")
    else:
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # API call
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": prompt}
            )

        if response.status_code == 200:
            data = response.json()

            if "answer" in data:
                answer = data["answer"]

                # Assistant message
                with st.chat_message("assistant"):
                    st.write(answer)

                    if "sources" in data:
                        st.caption(f"Sources: {data['sources']}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                st.error(data.get("error", "Unknown error"))
        else:
            st.error(f"API error: {response.status_code}")