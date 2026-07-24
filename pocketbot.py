import streamlit as st
import chat
import data
import tempfile
from pathlib import Path

st.title('Pocketbot - a local LLM assistant!')

uploaded_files = st.file_uploader(
    label="Please upload PDF or image file to create a personalised chatbot",
    accept_multiple_files=True,
)

create_bot = st.button("Create bot", disabled=not uploaded_files)

embeddings = data.create_embeddings()


if create_bot:
    with st.spinner(
            text='Please wait your personal assistant is loading...', show_time=True):
        temp_file_paths = []
        all_documents = []
        progress = 0
        # I utilised temporary files to bridge the gap between my previous path-reading functions and streamlit's UploadedFiles
    try:
        for uploaded_file in uploaded_files:
            suffix = Path(uploaded_file.name).suffix or ".tmp"
            with st.spinner(
                    text="Turning your files into useable Documents...", show_time=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    # creates a temporary file that will not be deleted immediately
                    temp_file.write(uploaded_file.getbuffer())
                    # A binary memory view of uploaded content is written to the temp file
                    temp_file_paths.append(temp_file.name)
                all_documents.extend(data.ocr_to_documents(
                    temp_file_paths[-1], dpi=100, min_confidence=40))

            # Extends the list of documents by using the OCR to Langchain document.
            # ocr_to_documents currently tuned for speed.

        if not all_documents:
            st.warning(
                "No OCR text could be extracted from the uploaded files.")
        else:
            with st.spinner(text='Creating chunks...', show_time=True):
                chunks = data.documents_get_chunks(all_documents)
            with st.spinner(text='Creating vectorstore...', show_time=True):
                data.create_vectorstore(chunks, embeddings)
            st.success(
                f"Vectorstore created from {len(uploaded_files)} file(s).")
            created = True
    finally:
        for temp_file_path in temp_file_paths:
            Path(temp_file_path).unlink(missing_ok=True)
    if not created:


"""
import streamlit as st

#with st.chat_message() #instet chat container

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

files = st.file_uploader()
"""
