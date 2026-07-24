from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from llm import create_llm
import streamlit


MAX_MEMORY_TURNS = 6
TOP_K_VECTORS = 3


def format_history(chat_history: List[Tuple[str, str]], max_turns: int = MAX_MEMORY_TURNS) -> str:
    """Format recent user and assistant turns into a memory block."""
    recent_history = chat_history[-max_turns:]
    current_lines = []
    for user_message, assistant_message in recent_history:
        current_lines.append(f"User: {user_message}")
        current_lines.append(f"Assistant: {assistant_message}")

    return "\n".join(current_lines)


def build_prompt(question: str, context: str, memory_block: str) -> str:
    """Create a prompt using retrieval context and recent conversation memory."""
    return (
        "You are a helpful assistant designed to answer questions. "
        "Use the retrieved context to inform your answers. "
        "If context is missing details, use conversation memory. "
        "If neither has the answer, say you are not sure.\n\n"
        f"Conversation memory:\n{memory_block if memory_block else 'No prior messages.'}\n\n"
        f"Retrieved context:\n{context}\n\n"
        f"Current user question:\n{question}\n\n"
        "Answer:"
    )


def format_context_with_metadata(docs: List[Document]) -> str:
    """Build context text that includes metadata for each retrieved chunk."""
    formatted_chunks: List[str] = []

    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        formatted_chunks.append(
            f"[Context {index}]\n"
            f"source: {source}\n"
            f"page: {page}\n"
            f"content:\n{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)


def ask_question(str) -> bool:
    return None


def chatbot() -> None:
    """ Run the chatbot"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        "vectorstores",
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print("Vectorstore loaded")

    llm = create_llm()

    print("Type your question. Type 'exit' to end chat.")
    while True:
        question = input(
            "Please enter your question or type 'exit' to exit: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "e"}:
            print("Goodbye")
            break

        docs = vectorstore.similarity_search(question, k=TOP_K_VECTORS)
        context = format_context_with_metadata(docs)
        memory_block = format_history(chat_history)
        prompt = build_prompt(question, context, memory_block)

        response = llm.invoke(prompt)
        print(f"Assistant: {response}\n")

        print("Sources used:")
        for index, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "unknown")
            print(f"{index}. source={source}, page={page}")
        print()

        chat_history.append((question, str(response)))


if __name__ == "__main__":
    chat_history = []
    chatbot()
