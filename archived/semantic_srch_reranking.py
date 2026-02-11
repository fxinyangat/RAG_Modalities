from sentence_transformers import SentenceTransformer, CrossEncoder, util

#.1 Bi-encoder

bi_model = SentenceTransformer('all-MiniLM-L6-v2')


#2. Cross-encoder (re-ranker)
cross_model  = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')

corpus = [
    "A man is eating food.",
    "A monkey is eating a banana.",
    "A professional athlete is playing soccer.",
    "Python is a popular programming language for data science.",
    "The internship CEO is a leadership fable for young professionals."
]

query = "What is Xavier's book about?"

corpus_embedding = bi_model.encode(corpus, convert_to_tensor=True)
query_embedding = bi_model.encode(query, convert_to_tensor=True)

results = util.semantic_search(query_embedding, corpus_embedding, top_k=5)[0]

# Re-ranking
print(f"Results: {results}")
cross_inp = [[query, corpus[result['corpus_id']]] for result in results]
cross_scores = cross_model.predict(cross_inp)

print(f"cross-scores:{cross_scores}")

#combine scores with their original text
for i in range(len(cross_scores)):
    results[i]['cross-score'] = cross_scores[i]

results = sorted(results, key=lambda x:x['cross-score'], reverse=True)

print(f"Query: {query}\n")

for result in results:
    text = corpus[result['corpus_id']]
    print(f"New score: {result['cross-score']:.4f} | Text {text}")


