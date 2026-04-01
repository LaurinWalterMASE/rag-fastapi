import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)


os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

UPLOAD_DIR = "uploads"
DB_DIR = "db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

persist_directory = "/opt/render/project/src/chroma_db"
vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embeddings,
    persist_directory=persist_directory
)


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        splits = splitter.split_documents(docs)

        # Store in vector DB
        vector_store.add_documents(splits)

        return {
            "status": "File uploaded & indexed",
            "filename": file.filename,
            "chunks": len(splits)
        }

    except Exception as e:
        return {"error": str(e)}



@app.post("/query")
async def query(req: dict):
    try:
        query_text = req.get("query")

        if not query_text:
            return {"error": "Query is required"}

        results = vector_store.similarity_search(query_text, k=5)

        if not results:
            return {"answer": "No relevant documents found"}

        context = "\n\n".join([doc.page_content for doc in results])

        prompt = f"""
Use ONLY the context below to answer.
If not found, say "I don't know".

Context:
{context}

Question:
{query_text}
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": [doc.metadata for doc in results]
        }

    except Exception as e:
        return {"error": str(e)}