"""Retrieval + Generation /Logic"""

from openai import OpenAI
import chromadb
import uuid
from dotenv import load_dotenv
from schema import Source, RAGResponse

load_dotenv()
class RAGEngine():
    def __init__(self):
        self.client = OpenAI()
        self.db = chromadb.PersistentClient(path="./dev_vector_db")
        self.collection = self.db.get_or_create_collection("book_project")

    def run(self, query: str, top_k: int):
        # Retrieval assuming we use chromas default embedding function

        results = self.collection.query(query_texts=[query], n_results=top_k)
        context = " ".join(results['documents'][0])

        #Generation

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer using the context provided."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
            temperature=0

    
        )
        return response.choices[0].message.content
    def run_with_citations(self, query: str, top_k:int, filter_filename: str =None):
        # Retrieva (Inlcude metadats)
        metadata_filter =None
        if filter_filename:
            metadata_filter = {"source": filter_filename}

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=metadata_filter,
            include=["documents", "metadatas", "distances"]
        )

       
        #2. Extract Context and source List
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]

        print(f"documents: {documents} \n citations:{metadatas}")

        context = "\n\n".join(documents)

        # Clean list of sources
        sources = [
            Source(filename=m['source'], content_snippet=d[:100] + '...') for d, m in zip(documents, metadatas)
        ]

        #Generation

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer using the context provided only. Do not use your internal training knowledgee."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
            temperature=0

    
        )
        return RAGResponse(
            answer=response.choices[0].message.content,
            sources=sources
        )





        # Ingest Documents to DB

    def ingest_new_document(self, text: str, filename: str):
        #use simple recursive chunking

        chunk_size = 1000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        # prepare metadata and IDs

        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": filename} for _ in chunks]

        # add tp Chrome Vector DB
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

        return {
            "message": "Chunks saved in vector db",
            "documents_save": len(chunks)
                 }
# RAGEngine().run_with_citations("what company policy say about vacation", 3)
