from data import create_embeddings, load_vectorstore
from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from langchain_ollama import OllamaLLM

import data

""" This script builds a local llm chatbot using the data pipeline. """


def create_llm_local():
    ''' Returns a particular OllamaLLM which has already been downloaded locally. '''

    llm = OllamaLLM(
        model="llama3.2:3b",
        temperature=0.2)
    print('LLM created!')

    return llm


def build_prompt(question: str, context: str, memory_block: str) -> str:
    """ Returns a useful prompt using retrieval context and recent conversation memory."""

    prompt = "You are a helpful assistant designed to answer questions." \
        "Use the retrieved context to inform your answers." \
        "If context is missing details, use the conversation memory." \
        "If neither has the answer, say you are not sure.\n\n" \
        f"Conversation memory:\n{memory_block if memory_block else 'No prior messages.'}\n\n" \
        f"Retrieved context:\n{context}\n\n" \
        f"Current user question:\n{question}\n\n" \
        "Answer:"

    return prompt


def format_history(chat_history: List[Tuple[str, str]], max_turns: int = 8) -> str:
    """Formats recent history of the conversation, ensuring it is only as long as the max_turns, to control the context window, 
    and turns it into a memory block consisting of the user's and assistant's messages."""
    recent_history = chat_history[-max_turns:]
    # Limits chat memory.
    current_lines = []
    for user_message, assistant_message in recent_history:
        current_lines.append(f"User: {user_message}")
        current_lines.append(f"Assistant: {assistant_message}")
    current_lines = "\n".join(current_lines)
    return current_lines


def format_context_with_metadata(docs: List[Document]) -> str:
    """Formats chunked langchain Documents into text that includes metadata for each retrieved chunk."""

    formatted_chunks = []

    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        formatted_chunks.append(
            f"[Context {index}]\nSource: {source}\nPage: {page}\nContent:\n{doc.page_content}")

    return "\n\n".join(formatted_chunks)


def chatbot(chat_history) -> None:
    """This function runs a chatbot that takes the previously created embeddings and vectorstore as well as a
    a pre downloaded LLM model and allows you to ask questions about the uploaded files."""

    # First a vectorstore needs to be created along with a llm.

    embeddings = data.create_embeddings()
    vectorstore = data.load_vectorstore(embedding_model=embeddings)
    llm = create_llm_local()

    # Now chat functionality can be implemented
    print("Please ask your question. Type 'exit' to end chat.")

    while True:
        question = input(
            "Please enter your question or type 'exit' to exit: ").strip()
        if not question:
            # Empty questions are disregarded
            continue
        if question.lower() in {"exit", "e"}:
            print("Goodbye")
            break

        # Similarity search returns the top k docs most similar to the user's question a key step of the RAG pipeline.
        docs = vectorstore.similarity_search(question, k=3)
        # Metadata is added to the retrieved documents so the chatbot can point to the sources of it's answers.
        context = format_context_with_metadata(docs)
        # A memory block is created with any chat history, could be empty initially.
        memory_block = format_history(chat_history)
        # Finally a prompt is made using the user's question, the retrieved context and the recent chat history.
        prompt = build_prompt(question, context, memory_block)

        # The pre-downloaded LLM is then fed the response and it is printed to the terminal
        response = llm.invoke(prompt)
        print(f"Assistant: {response}\n")

        # The Documents retrieved from the similarity search are printed with metadata to allow for easy user verification of the answers.
        print("Sources used:")
        for index, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "unknown")
            print(f"{index}. source={source}, page={page}")

        chat_history.append((question, str(response)))


if __name__ == "__main__":
    chat_history = []
    chatbot(chat_history)
    # llm = create_llm_local()
    # print(llm.invoke("Say hello in 5 words."))
