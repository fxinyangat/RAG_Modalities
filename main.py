"""Fast API wrapper takes request and returns a response"""

import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List, Union, Dict
from pydantic import BaseModel
from dotenv import load_dotenv
import io, PyPDF2
import pdfplumber

from engine import RAGEngine
from schema import Source, RAGResponse, QueryRequest


load_dotenv()

app = FastAPI(title = "Xavier RAG API", version="1.0.0")

# shema.py here

rag_engine = RAGEngine()

@app.get("/")
def read_root():
    return {"status": "RAG API is live"}

@app.post("/query", response_model=RAGResponse)
async def process_query(request: QueryRequest):

    try:
        if isinstance(request.query, list):
            # for simplicity lets loop , but best case is batch process

            results = [ rag_engine.run(q, request.top_k) for q in request.query] # or use .run_with_citations()

            return {"results": results}
        
        answer = rag_engine.run(request.query, request.top_k) 
        answer_with_citations = rag_engine.run_with_citations(request.query, request.top_k, request.filter_filename) 



        return answer_with_citations
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/ingest-file')
async def ingest_file(file: UploadFile = File(...)):
    # Accept .txt and .pdf and add it to Vector DB

    if not (file.filename.endswith('.txt') or file.filename.endswith('.pdf')):
        raise HTTPException(status_code=400, detail="Bad file. Only .txt and .pdf files allowed")
    
    try:
        # Read content
        content = await file.read()

        if file.filename.endswith('.pdf'):
            # extract pdf text
            # pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            with pdfplumber.open(io.BytesIO(content)) as pdf_reader:
                text = "".join([page.extract_text() for page in pdf_reader.pages])
        else:
            text = content.decode('utf-16')

    
        # chunk and save with engine
        num_chunkks = rag_engine.ingest_new_document(text, file.filename)

        print("Ingestion successfull")

        return {"filename": file.filename, "status": "success", "chunks_added": num_chunkks}
    
    except Exception as e:
        print(f"Error Ingesting:{e}")
        raise HTTPException(status_code=500, detail=f"File Ingestion failed: {e}")


            
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8686)




