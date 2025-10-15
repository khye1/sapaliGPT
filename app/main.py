import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.retriever import RAGRetriever

app = FastAPI(title="RAG Chatbot API")
retriever = RAGRetriever()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query trống")
    return retriever.answer(req.query)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
