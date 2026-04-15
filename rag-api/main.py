from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import httpx
import os

app = FastAPI(title="BrainIt RAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

async def get_embedding(text: str) -> list:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
    return response.json()["embedding"]

async def ask_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "phi3:mini", "prompt": prompt, "stream": False}
        )
    return response.json()["response"]

@app.get("/")
def root():
    return {"message": "BrainIt RAG API", "status": "alive"}

@app.post("/load")
async def load_documents():
    doc_dir = "./documents"
    loaded = []
    for filename in os.listdir(doc_dir):
        filepath = os.path.join(doc_dir, filename)
        with open(filepath, "r") as f:
            text = f.read()
        
        chunks = [text[i:i+500] for i in range(0, len(text), 400)]
        
        for idx, chunk in enumerate(chunks):
            doc_id = f"{filename}_{idx}"
            embedding = await get_embedding(chunk)
            collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": filename}]
            )
        loaded.append({"file": filename, "chunks": len(chunks)})
    
    return {"loaded": loaded, "total_documents": collection.count()}

@app.post("/ask")
async def ask(question: str):
    question_embedding = await get_embedding(question)
    
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    
    context = "\n\n".join(results["documents"][0])
    
    prompt = f"""Based ONLY on the following context, answer the question. If the context doesn't contain the answer, say "I don't have that information in my documents."

Context:
{context}

Question: {question}

Answer:"""
    
    answer = await ask_llm(prompt)
    
    return {
        "question": question,
        "answer": answer,
        "sources": results["metadatas"][0]
    }
