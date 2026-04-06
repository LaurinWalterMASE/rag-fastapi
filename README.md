# RAG FastAPI

THIS README WAS FULLY CREATED BY GITHUB COPILOT USING RAPTOR MINI (PREVIEW).

A Retrieval-Augmented Generation (RAG) demo application built with:
- `FastAPI` backend for file ingestion and query serving
- `Chroma` vector store for semantic retrieval
- `Google Generative AI` embeddings and chat model (`gemini-embedding-001` and `gemini-2.5-flash`)
- `React + Vite` frontend located in `rag-ui/`

## Project purpose

This repository demonstrates how to index PDF documents and answer natural language questions about them using semantic search and a generative model. Uploaded documents are converted into vector embeddings, stored in Chroma, and then retrieved to build a context-aware prompt for the Gemini chat model.

## Repository structure

- `app.py` - FastAPI backend exposing `/ingest` and `/query` endpoints
- `requirements.txt` - Python dependencies for the backend
- `runtime.txt` - runtime marker (typically used by deployment platforms)
- `rag-ui/` - React frontend application

## How it works

1. Upload a PDF file via `/ingest`.
2. The backend loads the PDF with `PyPDFLoader`.
3. The text is split into smaller chunks with `RecursiveCharacterTextSplitter`.
4. Chunks are indexed into a Chroma vector database.
5. Query requests are answered using similarity search results plus Gemini chat.

## Backend details

- Endpoint: `POST /ingest`
  - Accepts a file upload
  - Saves the file to `uploads/`
  - Indexes chunked PDF content into Chroma

- Endpoint: `POST /query`
  - Accepts JSON payload with `query`
  - Searches the vector store for the top 5 matching chunks
  - Sends the retrieved context to `ChatGoogleGenerativeAI`
  - Returns the generated answer and source metadata

## Requirements

- Python 3.11+
- `GEMINI_API_KEY` environment variable set before starting the backend

## Running locally

### Backend

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
python3 -m venv rag_env
source rag_env/bin/activate
pip install -r requirements.txt
```

3. Set the Gemini API key:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

4. Run the FastAPI server:

```bash
uvicorn app:app --reload
```

### Frontend

1. Change into the `rag-ui/` folder.
2. Install dependencies:

```bash
cd rag-ui
npm install
```

3. Start the Vite development server:

```bash
npm run dev
```

## Notes

- The backend currently allows CORS from all origins for development convenience.
- The Chroma persistence directory is configured in `app.py` at `/opt/render/project/src/chroma_db`.
- The frontend README is available in `rag-ui/README.md` and provides the default Vite+React template information.

## Future improvements

- Add authentication and secure CORS rules
- Support additional document types beyond PDF
- Add better prompt formatting with prompt templates
- Improve the frontend UI and error handling
