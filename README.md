# PDF-Reader-Chatbot
A llm chatbot which can converse about inputted PDFs.
## Plan
                PDF
                 |
                 ↓
        Extract text (PyPDF2)
                 |
                 ↓
        Split into chunks
 (CharacterTextSplitter)
                 |
                 ↓
        Create embeddings
 (OpenAIEmbeddings/HuggingFace)
                 |
                 ↓
        Store vectors
              FAISS
                 |
                 ↓
        User asks question
                 |
                 ↓
        Convert question to vector
                 |
                 ↓
        FAISS finds similar chunks
                 |
                 ↓
        Send chunks + question to LLM
                 |
                 ↓
             Answer

PDF
 ↓
PyPDF2
 ↓
RecursiveCharacterTextSplitter
 ↓
HuggingFaceEmbeddings
 ↓
FAISS
 ↓
Ollama
 ↓
Answer

User question
      |
      ↓
HuggingFaceEmbeddings
      |
      ↓
Question vector
      |
      ↓
FAISS similarity search
      |
      ↓
Relevant PDF chunks
      |
      ↓
Llama 3.2 via Ollama
      |
      ↓
Answer

? IVFPQ vectorisation FAISS