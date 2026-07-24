# Use python not python3
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import streamlit

# This pipeline turns a folder of PDFs and images into a FAISS vectorstore.

OCR_IMAGE_SUFFIXES = {".png", ".jpg",
                      ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


def files_to_vectorstore(path: str, embedding: HuggingFaceEmbeddings) -> FAISS:
    """Convert PDF input path into a saved FAISS vectorstore."""

    documents = pathpdf_to_documents(path)
    chunks = documents_get_chunks(documents)
    vectorstore = create_vectorstore(chunks, embedding)
    print('vectorstore created')
    return vectorstore


def ocrdata_to_page_text(ocr_data, min_confidence: int) -> str:
    """Return cleaned page text using only high-confidence OCR tokens."""
    tokens: List[str] = []
    for text, confidence in zip(ocr_data.get("text", []), ocr_data.get("conf", [])):
        cleaned_text = (text or "").strip()
        if not cleaned_text:
            continue

        try:
            conf_value = float(confidence)
        except (TypeError, ValueError):
            continue

        if conf_value >= min_confidence:
            tokens.append(cleaned_text)

    return " ".join(tokens).strip()


def ocr_to_documents(
    input_path: str,
    dpi: int = 250,
    psm: int = 6,
    min_confidence: int = 60,
) -> List[Document]:
    """Load PDFs with OCR and return LangChain Document objects.

    Args:
        pdf_input: Path to a folder or file containing PDF and image files.
        dpi: Render resolution for PDF-to-image conversion before OCR, 300 is a common baseline so 250 is slightly faster.
        psm: Tesseract page segmentation mode used for text layout parsing, 6 is for 'normal' document blocks.
        min_confidence: Minimum OCR confidence score required to keep a token, 60 is more thank likely not noise.
    """
    source_path = Path(input_path)
    if source_path.is_dir():
        file_paths = sorted(
            path
            for path in source_path.iterdir()
            if path.is_file() and (path.suffix.lower() == ".pdf" or path.suffix.lower() in OCR_IMAGE_SUFFIXES)
        )
    elif source_path.is_file() and (
        source_path.suffix.lower() == ".pdf" or source_path.suffix.lower() in OCR_IMAGE_SUFFIXES
    ):
        file_paths = [source_path]
    else:
        raise ValueError(
            f"Expected a PDF/image file or folder containing OCR-supported files: {input_path}")

    documents: List[Document] = []
    config = f" --psm {psm}"

    for source_file_path in file_paths:
        suffix = source_file_path.suffix.lower()
        loaded_pages = 0

        print(f"Starting OCR for: {source_file_path}")

        if suffix == ".pdf":
            page_images = convert_from_path(str(source_file_path), dpi=dpi)
        else:
            page_images = [Image.open(source_file_path)]

        total_pages = len(page_images)
        print(f"Rendered {total_pages} page image(s) for OCR.")

        for page_number, image in enumerate(page_images, start=1):
            if page_number == 1 or page_number % 10 == 0 or page_number == total_pages:
                print(
                    f"OCR progress: page {page_number}/{total_pages} for {source_file_path.name}")

            ocr_data = pytesseract.image_to_data(
                image,
                config=config,
                output_type=pytesseract.Output.DICT,
            )

            page_text = ocrdata_to_page_text(ocr_data, min_confidence)
            if not page_text:
                continue

            loaded_pages += 1
            documents.append(
                Document(
                    page_content=page_text,
                    metadata={
                        "source": str(source_file_path),
                        "page": page_number,
                        "extraction": "ocr",
                        "file_type": suffix.lstrip("."),
                    },
                )
            )

        if loaded_pages == 0:
            print(f"No OCR text found in:\n {source_file_path}.")
        else:
            print(
                f"OCR extracted text from:\n {source_file_path}\n With text from {loaded_pages} pages.")

    if len(documents) > 0:
        print(f"{len(documents)} OCR langchain Documents created!")
    else:
        print("No OCR documents created")

    return documents


def documents_get_chunks(documents: List[Document]) -> List[Document]:
    """Split Documents into overlapping chunks for retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print("Chunks created!")
    return chunks


def create_vectorstore(chunks: List[Document], embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """Create a FAISS vectrostore from chunked documents."""
    print(
        f"Building FAISS index from {len(chunks)} chunk(s). This can take time on CPU.")
    vectorstore = FAISS.from_documents(
        documents=chunks, embedding=embedding_model)
    vectorstore.save_local("vectorstores")
    print("Vector database created!")
    return vectorstore


def ocr_to_vectorstore(
    path: str,
    embedding: HuggingFaceEmbeddings,
    dpi: int = 300,
    psm: int = 6,
    min_confidence: int = 60,
) -> FAISS:
    """Convert PDF input path into a saved FAISS vectorstore using OCR text extraction."""
    print("Stage 1/3: OCR document extraction")
    documents = ocr_to_documents(
        input_path=path,
        dpi=dpi,
        psm=psm,
        min_confidence=min_confidence,
    )
    print("Stage 2/3: Text chunking")
    chunks = documents_get_chunks(documents)
    print("Stage 3/3: Embedding + FAISS indexing")
    vectorstore = create_vectorstore(chunks, embedding)
    print('OCR vectorstore created')
    return vectorstore


def load_vectorstore(embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """Load a FAISS vectorstore from local storage."""
    vectorstore = FAISS.load_local(
        "vectorstores", embedding_model, allow_dangerous_deserialization=True)
    print("Vectorstore created!")
    return vectorstore


def create_embeddings() -> HuggingFaceEmbeddings:
    """Create embedding model used by FAISS vectorstore."""
    print("Loading embedding model sentence-transformers/all-MiniLM-L6-v2...")
    embedding_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2')
    print("Embedding created!")
    return embedding_model


if __name__ == "__main__":
    pdf_path = Path(
        r"C:\Users\Oliver Washbrook\OneDrive\Documents\Code\PDFchatbot\Baking PDFs")

    embeddings = create_embeddings()

    ocr_to_vectorstore(pdf_path, embeddings)


"""
Archived old pdf reader function, kept as OCR is slow.


def pathpdf_to_documents(pdf_input: str) -> List[Document]:
    Load one PDF or a folder of PDFs into LangChain Document objects
    input_path = Path(pdf_input)
    if input_path.is_dir():
        pdf_paths = sorted(input_path.glob("*.pdf"))
    elif input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_paths = [input_path]
    else:
        raise ValueError(f"Expected a PDF file or folder of PDFs: {pdf_input}")

    documents = []

    for source_pdf_path in pdf_paths:
        pdf_reader = PdfReader(source_pdf_path)
        total_pages = 0
        unloaded_pages = 0
        loaded_pages = 0
        for page_number, page in enumerate(pdf_reader.pages):
            total_pages += 1
            text = page.extract_text() or 0
            if text == 0:
                unloaded_pages += 1 
            else:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": str(source_pdf_path), "page": page_number + 1},
                    )
                )
                loaded_pages += 1
        if loaded_pages == 0:
            print(f"No text found in  \n {source_pdf_path}. ")
        elif loaded_pages > 0:
            print(f"Extracted text from: \n {source_pdf_path} \n With text from {loaded_pages} pages.")       
    if len(documents) > 0:  
        print(f"{len(documents)} langchain Documents created!")
    else:
        print("Error documents failed to load")
    return documents
"""
