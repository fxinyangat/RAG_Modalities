from sentence_transformers import SentenceTransformer, util

# load a pretrained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# corpus

corpus = [
    "A man is eating food.",
    "A monkey is eating a banana.",
    "A professional athlete is playing soccer.",
    "Python is a popular programming language for data science.",
    "The internship CEO is a leadership fable for young professionals."
]

query = "What is Xavier's book about?"

# encode query and corpus

query_embeddings = model.encode(query, convert_to_tensor=True)

corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

results = util.semantic_search(query_embeddings, corpus_embeddings, top_k=2)

print(f"Query: {query} \n Results: {results}")

print(f"First Answer: {corpus[results[0][0]['corpus_id']]}")
print(f"Second Answer: {corpus[results[0][1]['corpus_id']]}")



