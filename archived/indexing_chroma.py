import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

documents = [
    
        "The cat is on the mat",
        "The weather is sunny",
        "The internship CEO is a leadership fable for young professionals.",
        "Xavier Inyangat moved to the U.S. to study AI at ASU."
    
]

metadata =[{"type": "animals", "catehory": "homes"},
           {"type": "news", "category": "weather"},
           {"type": "memoirs", "category": "education"},
           {"type":"memoirs", "catehory": "people and culture"}
           
           ]

# initialize
client = chromadb.PersistentClient(path="./my_vector_db")

#2. Define embedding function

model = 'all-MiniLM-L6-v2'

myEmbeddingFunction = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)

# class MyEmbeddingFunction:
#     def __call__(self, input: list[str]) -> list[list[float]]:
#         return model.encode(input).tolist()

# 3. Get/Create collection 
collection = client.get_or_create_collection(
    name="book_project",
    embedding_function=myEmbeddingFunction
)

#4. Ingest the data
def ingest_data():

    ids = [f"id_{i}" for i in range(len(documents))]

    collection.add(documents=documents,metadatas=metadata, ids=ids)
    print(f"Successfully indexed {len(documents)} documents")

# Retrieval Loop

def search_data(query_text):
    results = collection.query(
        query_texts=[query_text],
        where={"type": "memoirs"},
        n_results=3
    )
    return results

### ACTION

ingest_data()


user_query = "Who Studied at Arizona State University?"
hits = search_data(user_query)

print(f"Hits: {hits}")

print(f"\nQuery: {user_query}")
for i,doc in enumerate(hits['documents'][0]):
    print(f"Match {i+1}: {doc} (Distance: {hits['distances'][0][i]:.4f})")



