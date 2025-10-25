"""Retrieve related content from vector database using cosine similarity."""

from langchain_chroma import Chroma
from embed_fn import embedding
import os

class RetrieveContentFromVectorStore:
    def __init__(self, sessionID):
        self.sessionID = sessionID
        self.vectorstore = Chroma(
            collection_name=self.sessionID,
            embedding_function=embedding,
            chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )

    def get_content(self, query):
        try:
            content = self.vectorstore.similarity_search(
                query, k= 2
            )
            return "\n".join([con.page_content for con in content])
        except Exception as e:
            print(f"Error: {e}")
            return ""
