import streamlit as st
import chat
import data
import tempfile
from pathlib import Path

"""This script runs a locally hosted streamlit server to provide a UI to the assistant chatbot."""

st.title('Welcome to a personal LLM assistant PDF reader!')

uploaded_files = st.file_uploader(
    label="Please upload PDF or image file and press the button to create a personalised chatbot!",
    accept_multiple_files=True)

create_bot = st.button("Create bot", disabled=not uploaded_files)

embeddings = data.create_embeddings()

# Initialise session state which will store the chat history, vectorstore and llm for later use.

if 'user' not in st.session_state:
    st.session_state['user'] = []

if 'assistant' not in st.session_state:
    st.session_state['assistant'] = []

if 'chatbot_ready' not in st.session_state:
    st.session_state['chatbot_ready'] = False

if 'vectorstore' not in st.session_state:
    st.session_state['vectorstore'] = None

if 'llm' not in st.session_state:
    st.session_state['llm'] = None

# Once the button is pressed

if create_bot:

    created_vectorstore = False
    vectorstore = None

    with st.spinner(text='Please wait your personal assistant is loading...', show_time=True):

        # Temporary files to bridge the gap between path-reading functions and streamlit's UploadedFiles.

        temp_file_paths = []
        document_list = []

    try:
        for uploaded_file in uploaded_files:
            suffix = Path(uploaded_file.name).suffix or ".tmp"

            with st.spinner(text="Turning your files into useable Documents... Please be patient...", show_time=True):

                # Creates a temporary file that will not be deleted immediately
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    # A binary memory view of uploaded content is written to the temporary file
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_paths.append(temp_file.name)
                # The document list is extended, with the below parameters chosen for speed
                document_list.extend(data.ocr_to_documents(
                    temp_file_paths[-1], dpi=100, min_confidence=40))

        if not document_list:
            st.warning(
                "No OCR text could be extracted from the uploaded files!")

        else:
            with st.spinner(text='Creating chunks...', show_time=True):
                chunks = data.documents_get_chunks(document_list)

            with st.spinner(text='Creating vectorstore...', show_time=True):
                vectorstore = data.create_vectorstore(chunks, embeddings)

            st.success(
                f"Vectorstore created from {len(uploaded_files)} file(s).")
            created_vectorstore = True

    finally:
        # Delete temporary files after use.
        for temp_file_path in temp_file_paths:
            Path(temp_file_path).unlink(missing_ok=True)

    if created_vectorstore and vectorstore is not None:
        st.session_state['vectorstore'] = vectorstore
        st.session_state['chatbot_ready'] = True
        st.session_state['llm'] = chat.create_llm_local()
        st.success('Chatbot created!')

# Once the chatbot and vectorstore have been created.

if st.session_state['chatbot_ready'] and st.session_state['vectorstore'] is not None:

    # Update the UI chat every rerun of the script
    for user_message, assistant_message in zip(st.session_state['user'], st.session_state['assistant']):
        with st.chat_message("user"):
            st.markdown(user_message)
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

    question = st.chat_input(
        "Welcome to your custom assistant. Please ask a question about your uploaded documents")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        docs = st.session_state['vectorstore'].similarity_search(question, k=5)

        context = chat.format_context_with_metadata(docs)

        # Compile memory from the last 8 completed user/assistant turns.
        recent_turns_user = st.session_state['user'][-8:]
        recent_turns_assistant = st.session_state['assistant'][-8:]
        recent_turns = list(zip(recent_turns_user, recent_turns_assistant))
        memory_block = chat.format_history(recent_turns, max_turns=8)

        prompt = chat.build_prompt(
            question=question, context=context, memory_block=memory_block)

        response = st.session_state['llm'].invoke(prompt)
        response_text = str(response)

        # Captures history and updates UI chat
        st.session_state['user'].append(question)
        st.session_state['assistant'].append(response_text)

        with st.chat_message("assistant"):
            st.markdown(response_text)
