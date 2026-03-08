from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils import embedding_functions


load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

## instantiate the embedding function (uses oopen ai to generate embeddings)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key = openai_key,
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path="chroma_vector_db")
collection = chroma_client.get_or_create_collection(name="my_news_collection", embedding_function=openai_ef)




## Load Documents from a directory

def load_documents_from_directory(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(
                os.path.join(directory_path, filename)
            ) as file:
                documents.append({"id": filename, "text": file.read()})
    return documents

## split documents into chucks

def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start = end - chunk_overlap

    return chunks

## Load documents from directory

directory_path = "./news_articles"

documents = load_documents_from_directory(directory_path)

print(f"Loaded {len(documents)} documents")

## split documents into chunks

chunked_documents = []

for doc in documents:
    chunks = split_text(doc["text"])
    print(f"Splitting {doc['id']} into chunks")

    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})

print(f"Split documents into {len(chunked_documents)} chunks")

## Function to generate embeddings
def get_openai_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding

    return embedding

## Generate embeddings for the document chunks

for doc in chunked_documents:

    print("---Generating embedding...---")

    doc["embedding"] = get_openai_embedding(doc["text"])

## Upsert documents with embeddings into Chroma DB

for doc in chunked_documents:
    print("==== Inserting into Vector DB...====")
    collection.upsert(
        ids= [doc['id']],
        documents= [doc['text']],
        embeddings=[doc['embedding']]
    )


# Function to query Documents

def query_documents(question, n_results):
    results = collection.query(query_texts=question, n_results=n_results)

    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    return relevant_chunks


# Function to generate response

def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = client.chat.completions.create(
        model="gpt-5.4-2026-03-05",
        messages=[{
              "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": question
        }

        ]
    )
    answer = response.choices[0].message
    return answer


# Example
question = "what are the impacts of AI on sucide rates?"
relevant_chunks = query_documents(question, n_results=5)
answer = generate_response(question, relevant_chunks)

print(answer.content)
