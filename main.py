# Use python not python3
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def pdf_to_documents(PDF):
    # Read PDF and create langchain document with metadata
    pdf_reader = PdfReader(PDF)
    documents = []
    for page_number , page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            documents.append(Document(page_content= text , metadata={"source" : str(PDF), "page": page_number + 1}))
    return documents

####
def clean_text(text):

    text = text.replace("\u2028", "\n")
    text = text.replace("\u2029", "\n")

    return text
####

print('***')
breads_path = Path(__file__).parent / 'Baking PDFs' / \
    'Keto-Breads-Digital-Version_Spreads_Upload (9).pdf'
KETOBreadDocuments = pdf_to_documents(breads_path)
print(f'{len(KETOBreadDocuments)} PDF pages loaded')

#print(KETOBreadDocuments[50:53])

def documents_get_chunks(documents):
    # Takes langchain documents and creates chunks from them
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return chunks

KETOBreadChunks = documents_get_chunks(KETOBreadDocuments)
#print(KETOBreadChunks[50:55])

# Core of RAG pipeline need to create embeddings and vectors into FAISS

def create_embeddings():
    embeddings = HuggingFaceEmbeddings( model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

embeddings = create_embeddings()

def create_vectorstore(name, chunks):

    vectorstore = FAISS.from_documents(documents = chunks , embedding = embeddings)
    vectorstore.save_local(f"vectorstores/{name}")
    print("vector database created!")
    return vectorstore

# Run once:
# KETOBreadVectorstore = create_vectorstore("keto",KETOBreadChunks) 

def load_vectorstore(): 
    embeddings
    vectorstore = FAISS.load_local("vectorstore",embeddings,allow_dangerous_deserialization=True)
    return vectorstore

vectorstore = load_vectorstore()


print('*****')
