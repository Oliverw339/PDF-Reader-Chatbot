## Reader Chatbot Assistant 


### Project overview

This project is a local RAG assistant for PDFs and images. Users upload files in a Streamlit UI, OCR extracts text, and a local LLM answers questions using retrieved document context.

The codebase is split into three parts:
- `data.py`: OCR, chunking, embeddings, and FAISS index creation.
- `chat.py`: prompt construction, retrieval context formatting, and conversation memory.
- `app.py`: Streamlit interface and session state orchestration.

The design is local-first for privacy, offline use, and low running cost.

### Data pipeline

The pipeline extracts text with Tesseract OCR, converts output to LangChain documents, splits documents into overlapping chunks, embeds those chunks, and stores them in FAISS.

Current model choices:
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Vector index: FAISS (fast local similarity search)

This setup is efficient for local retrieval workflows, though OCR speed remains a bottleneck.


### Chatbot

The chatbot retrieves the most relevant chunks from FAISS for each query, builds a prompt with retrieval context plus recent chat history, and generates an answer with a local Ollama model.

Current generation model: `llama3.2:3b`.

Running locally improves privacy and avoids API fees, with the trade-off of lower model capacity compared with large hosted models.


### App

The app is built with Streamlit and uses temporary files to bridge uploaded content with the existing path-based OCR pipeline.

Session state stores the LLM, vectorstore, and chat history. Chat UX is stable, but retrieved chunk metadata visibility in the UI can still be improved.


### Future work

#### Upgrading the data ingestion pipeline

- Add layout-aware document understanding (for example, CV-based extraction) for complex pages.
- Improve OCR performance or evaluate alternate OCR engines.
- Reduce setup friction around Tesseract/Poppler dependencies.
- Add computer vision capability for non-text data. 

#### Deploying to the cloud
- Deploy to Streamlit Community Cloud.
- Migrate local model dependencies to hosted inference.
- Revisit provider options (Hugging Face, OpenAI, others) based on compatibility and cost.
- Plan around Community Cloud resource limits.

#### Optimisation

- Tune chunk size/overlap and OCR settings (DPI, PSM).
- Add an evaluation framework for answer quality (accuracy, relevance, consistency).

- Investigate document-specific adaptation or fine-tuning strategies.

#### Other 

- Allow users to choose between multiple LLM and embedding model options.

## Repository Structure

```
PDFchatbot/
|- app.py                # Streamlit UI entrypoint
|- chat.py               # Prompting, conversation memory, and CLI chatbot
|- data.py               # OCR, chunking, embeddings, and FAISS index creation
|- requirements.txt      # Python dependencies
|- README.md
|- Baking PDFs/          # Example input files
`- vectorstores/         # Saved FAISS index files
```

Notes:
- `app.py` is the main app you run for the web interface.
- `chat.py` can also run standalone as a terminal chatbot.
- `data.py` builds the retrieval index used by both app modes.


## How It Works

1. Upload one or more PDF/image files in the Streamlit app.
2. Files are temporarily written to disk so path-based OCR functions can process them.
3. OCR extracts text page-by-page (Tesseract via `pytesseract`, PDF rendering via `pdf2image`).
4. Extracted text is converted into LangChain `Document` objects with metadata such as source and page.
5. Documents are split into overlapping chunks (`RecursiveCharacterTextSplitter`).
6. Chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2`.
7. Embeddings are indexed in a FAISS vectorstore.
8. At question time, a similarity search retrieves the top matching chunks.
9. Retrieved chunk text + recent chat history are used to build a prompt.
10. A local Ollama model (`llama3.2:3b`) generates the response.

The result is a local RAG workflow: retrieval provides grounded context, and the LLM answers based on that context.


## Setup

### 1. Prerequisites

- Python 3.10+ (3.11 recommended)
- Tesseract OCR installed and available on PATH
- Poppler installed and available on PATH (required by `pdf2image` for PDFs)
- Ollama installed with model pulled locally:

```powershell
ollama pull llama3.2:3b
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Build a vectorstore (optional CLI pre-build)

If you want to prebuild from files in `Baking PDFs/`:

```powershell
python data.py
```

### 5. Run the Streamlit app

```powershell
streamlit run app.py
```

Then upload documents, click **Create bot**, and start asking questions.

### 6. Run CLI mode (optional)

```powershell
python chat.py
```

### Troubleshooting

- If OCR fails on PDFs, verify Poppler binaries are installed and on PATH.
- If OCR fails generally, verify Tesseract is installed and on PATH.
- If model calls fail, ensure Ollama is running and `llama3.2:3b` is available locally.
