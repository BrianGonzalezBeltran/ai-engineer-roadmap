from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="BrainIt AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.get("/")
def root():
    return {"message": "BrainIt AI API", "status": "alive"}

@app.post("/chat")
async def chat(prompt: str):
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        })
    return {"prompt": prompt, "response": response.json()["response"]}
