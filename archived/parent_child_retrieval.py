import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer, util
import uuid


# init client and model

client = chromadb.PersistentClient(path="./parent_child_db")
# model = SentenceTransformer("all-MiniLM-L6-v2")
model ="all-MiniLM-L6-v2"

# class SimpleEmbeddingFunction:
#     def __call__(self, input: list[str]) -> list[list[float]]:
#         return model.encode(input).tolist()

collection = client.get_or_create_collection(
    name="hierarchical_rag",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
)

# 1. THE DATA (A long section from 'The Intern CEO')
parent_text = """
The Intern CEO leadership framework is built on three pillars: Radical Ownership, 
Systems Thinking, and the Growth Mindset. Radical Ownership means taking 100% 
responsibility for outcomes, even those outside your direct control. 
Systems Thinking involves understanding how small coding changes affect the 
entire AI architecture. Growth Mindset is the belief that skills are built through 
persistence rather than innate talent.
"""

# 2. THE INDEXING STRATEGY
# We store the 'Parent' in a dictionary (or separate DB) for retrieval
parent_id = str(uuid.uuid4())
parent_store = {parent_id: parent_text}

# We split the parent into small 'Child' chunks (sentences)
children = [
    "Radical Ownership means taking 100% responsibility for outcomes.",
    "Systems Thinking involves understanding AI architecture impacts.",
    "Growth Mindset is the belief that skills are built through persistence."
]

# Add children to Vector DB, but link them to the Parent ID in metadata
collection.add(
    documents=children,
    ids=[str(uuid.uuid4()) for _ in children],
    metadatas=[{"parent_id": parent_id} for _ in children]
)

# 3. THE RETRIEVAL STRATEGY
query = "What does the book say about taking responsibility?"
results = collection.query(query_texts=[query], n_results=1)

# Instead of showing the child match, we look up the parent
matched_metadata = results['metadatas'][0][0]
actual_parent_id = matched_metadata['parent_id']

print(f"Query: {query}")
print(f"Matched Child: {results['documents'][0][0]}")
print(f"\n--- CONTEXT SENT TO LLM ---")
print(parent_store[actual_parent_id])