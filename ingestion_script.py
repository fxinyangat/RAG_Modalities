from sentence_transformers import SentenceTransformer, util
from chromadb.utils import embedding_functions
import chromadb

client = chromadb.PersistentClient('./dev_vector_db')
model = 'all-MiniLM-L6-v2'

myEmbeddingFunction = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)

collection = client.get_or_create_collection(
    name="book_project",

    embedding_function=myEmbeddingFunction
)

documents = [
    "Xavier Inyangat is an AI Engineer and Data Scientist.",
    "The Internship CEO is a book about leadership for young professionals.",
    "RAG stands for Retrieval-Augmented Generation."
]

ids = [f"id_{indx+1}" for indx in range(len(documents))]

collection.add(documents=documents, ids=ids)

print(f"{len(documents)} documents ingestion completed. Your API is read to retrieve")

