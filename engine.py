"""Retrieval + Generation /Logic"""

from openai import OpenAI
import chromadb

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