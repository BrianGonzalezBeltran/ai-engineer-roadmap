from fastapi import FastAPI, Query
from datetime import datetime

app = FastAPI(title="Brian's AI Engineer API", version="0.2.0")

projects = [
    {
        "id": 1,
        "name": "Data Warehouse SDDE",
        "description": "Built a data warehouse from scratch using MS Fabric",
        "tech": ["Python", "SQL", "MS Fabric"],
        "status": "in progress"
    },
    {
        "id": 2,
        "name": "RAG System",
        "description": "Question answering system over documents using LLMs",
        "tech": ["Python", "FastAPI", "LangChain", "ChromaDB"],
        "status": "planned"
    }
]

@app.get("/")
def root():
    return {"message": "Welcome to brainit.run", "status": "alive"}

@app.get("/about")
def about():
    return {
        "name": "Brian González Beltrán",
        "role": "AI Engineer in progress",
        "background": "Industrial Engineer - Universidad de los Andes",
        "focus": ["RAG systems", "LLM integration", "MLOps"],
        "server_time": datetime.now().isoformat()
    }

@app.get("/projects")
def get_projects(status: str = Query(default=None)):
    if status:
        return [p for p in projects if p["status"] == status]
    return projects

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for p in projects:
        if p["id"] == project_id:
            return p
    return {"error": "Project not found"}
