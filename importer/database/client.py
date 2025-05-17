from typing import Optional
import requests
import os
import uuid

CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma-db")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
BASE_URL = f"http://{CHROMA_HOST}:{CHROMA_PORT}/api/v1"

class ChromaClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
    
    def create_collection(self, name: str) -> Optional[str]:
        """Создаем коллекцию и возвращаем её ID"""
        response = self.session.post(
            f"{BASE_URL}/collections",
            json={
                "name": name,
                "metadata": {
                    "hnsw:space": "cosine",
                    "embedding_function": "custom"    
                }
            },
            headers=self.headers
        )
        return response.json().get("id") if response.ok else None

    def get_collection(self, name: str) -> Optional[str]:
        """Получаем ID коллекции по имени"""
        response = self.session.get(f"{BASE_URL}/collections")
        if response.ok:
            for collection in response.json():
                if collection["name"] == name:
                    return collection["id"]
        return None

    def get_or_create_collection(self, name: str) -> str:
        """Получаем или создаем коллекцию"""
        collection_id = self.get_collection(name)
        if not collection_id:
            collection_id = self.create_collection(name)
        return collection_id

    def add_documents(self, collection_id: str, documents: list, metadatas: list, embeddings: list):
        """Добавляем документы в коллекцию"""
        payload = {
            "ids": [str(uuid.uuid4()) for _ in documents],
            "documents": documents,
            "metadatas": metadatas,
            "embeddings": embeddings
        }
        
        response = self.session.post(
            f"{BASE_URL}/collections/{collection_id}/add",
            json=payload,
            headers=self.headers
        )
        return response.json() if response.ok else None