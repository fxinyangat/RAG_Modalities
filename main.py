"""Fast API wrapper takes request and returns a response"""

import os
from fastapi import FastAPI, HTTPException
from typing import List, Union
from pydantic import BaseModel
from dotenv import load_dotenv

from engine import RAGEngine

load_dotenv()

app = FastAPI(title = "Xavier RAG API", version="1.0.0")

# The request schema
class QueryRequest(BaseModel):
    query: Union[str, list[str]]
    model: str = "gpt-4o-mini"
    top_k: int = 3

rag_engine = RAGEngine()

@app.get("/")
def read_root():
    return {"status": "RAG API is live"}

@app.post("/query")
def process_query(request: QueryRequest):

    try:
        if isinstance(request.query, list):
            # for simplicity lets loop , but best case is batch process

            results = [ rag_engine.run(q, request.top_k) for q in request.query]

            return {"results": results}
        
        answer = rag_engine.run(request.query, request.top_k)

        return {"query": request.query, "answer": answer}
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8686)




