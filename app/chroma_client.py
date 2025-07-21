import chromadb
from chromadb.api.types import Documents, Embeddings, IDs, Metadatas
from sentence_transformers import SentenceTransformer
import os

class ChromaDBClient:
    def __init__(self, collection_name="pdf_chunks"):
        chroma_host = os.getenv("CHROMA_HOST", "chroma-db")
        chroma_port = os.getenv("CHROMA_PORT", "8000") 
        self.client = chromadb.HttpClient(host=chroma_host, port=int(chroma_port), ssl=False, headers=None)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_chunks(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        embeddings = self.embedder.encode(texts).tolist()
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, paper_id, query_text: str, k=3):
        query_embedding = self.embedder.encode([query_text]).tolist()
        return self.collection.query(query_embeddings=query_embedding, n_results=k, where={"paper_id": paper_id})
