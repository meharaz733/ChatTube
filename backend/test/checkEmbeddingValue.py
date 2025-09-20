from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# reconnect to the same collection
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectorStore = Chroma(
    collection_name="be46d191-cd2d-4cdf-8d1d-3e7aa70257a4",
    embedding_function=embedding,
    chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
)

# Fetch one document with its embedding
results = vectorStore.get(
    ids=["c6b6663b-db21-44e4-a694-e0dd74c1a26b"],   # replace with your real ID
    include=["embeddings", "documents", "metadatas"]
)

print(results)
print("Document:", results["documents"])
print("Embedding length:", len(results["embeddings"]))
print("First 10 values:", results["embeddings"])
