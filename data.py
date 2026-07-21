# Use python not python3
from pathlib import Path
from typing import List, Sequence, Union

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def pathpdf_to_documents(pdf_input: Union[str, Path]) -> List[Document]:
    """Load one PDF or a folder of PDFs into LangChain Document objects"""
    input_path = Path(pdf_input)
    if input_path.is_dir():
        pdf_paths = sorted(input_path.glob("*.pdf"))
    elif input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_paths = [input_path]
    else:
        raise ValueError(f"Expected a PDF file or folder of PDFs: {pdf_input}")

    documents: List[Document] = []
    total_pages = 0

    for source_pdf_path in pdf_paths:
        pdf_reader = PdfReader(source_pdf_path)
        for page_number, page in enumerate(pdf_reader.pages):
            total_pages += 1
            text = page.extract_text()
            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": str(source_pdf_path), "page": page_number + 1},
                    )
                )
    print(f"{total_pages} PDF pages turned into langchain Documents!")
    return documents



def documents_get_chunks(documents: Sequence[Document]) -> List[Document]:
    """Split Documents into overlapping chunks for retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print("Chunks created!")
    return chunks



def create_vectorstore(chunks: Sequence[Document], embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """Create a FAISS vectrostore from chunked documents."""

    vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)
    vectorstore.save_local("vectorstores")
    print("Vector database created!")
    return vectorstore

def files_to_vectorstore(path: Union[str, Path], embedding: HuggingFaceEmbeddings) -> FAISS:
    """Convert PDF input path into a saved FAISS vectorstore."""

    documents = pathpdf_to_documents(path)
    chunks = documents_get_chunks(documents)
    vectorstore = create_vectorstore(chunks, embedding)
    print('vectorstore created')
    return vectorstore


def load_vectorstore(embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """Load a FAISS vectorstore from local storage."""
    vectorstore = FAISS.load_local("vectorstores", embedding_model, allow_dangerous_deserialization=True)
    print("Vectorstore created!")
    return vectorstore

def create_embeddings() -> HuggingFaceEmbeddings:
    """Create embedding model used by FAISS vectorstore."""
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    print("Embedding created!")
    return embedding_model

if __name__ == "__main__":
    pdf_path = Path(r"C:\Users\Oliver Washbrook\OneDrive\Documents\Code\PDFchatbot\Baking PDFs")

    embeddings = create_embeddings()

    files_to_vectorstore(pdf_path, embeddings)

    print('*****')

