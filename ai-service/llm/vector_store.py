from sentence_transformers import SentenceTransformer
import httpx
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import json
import logging
from config.settings import get_settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            # Получаем настройки из settings.py
            settings = get_settings()
            logger.info(f"Настройки ChromaDB из settings: host={settings.CHROMA_HOST}, port={settings.CHROMA_PORT}")
            
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Модель SentenceTransformer загружена")
            
            # Настройки подключения к ChromaDB из settings
            self.host = settings.CHROMA_HOST
            self.port = settings.CHROMA_PORT
            self.base_url = f"http://{self.host}:{self.port}/api/v1"
            self.collection_name = "crocodile"
            self.collection_id = None  # UUID коллекции будет получен при инициализации
            
            logger.info(f"ChromaDB connection settings: host={self.host}, port={self.port}, base_url={self.base_url}")
            
            # Инициализация HTTP клиента
            self.client = httpx.Client(timeout=30.0)
            
            # Получаем UUID коллекции и проверяем её существование
            self._ensure_collection_exists()
            logger.info("VectorStore успешно инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации VectorStore: {str(e)}", exc_info=True)
            raise

    def _get_collection_id(self) -> str:
        """Получает UUID коллекции по имени"""
        try:
            logger.info(f"Получаем UUID коллекции {self.collection_name}")
            response = self.client.get(
                f"{self.base_url}/collections",
                params={"tenant": "default_tenant", "database": "default_database"}
            )
            response.raise_for_status()
            
            collections = response.json()
            for collection in collections:
                if collection["name"] == self.collection_name:
                    collection_id = collection["id"]
                    logger.info(f"Найден UUID коллекции {self.collection_name}: {collection_id}")
                    return collection_id
                    
            raise ValueError(f"Коллекция {self.collection_name} не найдена")
            
        except Exception as e:
            logger.error(f"Ошибка при получении UUID коллекции: {str(e)}", exc_info=True)
            raise

    def _ensure_collection_exists(self):
        """Проверяет существование коллекции и создает её при необходимости"""
        try:
            # Получаем UUID коллекции
            self.collection_id = self._get_collection_id()
            logger.info(f"Коллекция {self.collection_name} существует (UUID: {self.collection_id})")
                
        except ValueError as e:
            # Если коллекция не найдена, создаем её
            logger.info(f"Коллекция {self.collection_name} не найдена, создаем...")
            create_response = self.client.post(
                f"{self.base_url}/collections",
                params={"tenant": "default_tenant", "database": "default_database"},
                json={
                    "name": self.collection_name,
                    "metadata": {"hnsw:space": "cosine"},
                    "dimension": 384  # Размерность модели all-MiniLM-L6-v2
                }
            )
            create_response.raise_for_status()
            # После создания получаем UUID
            self.collection_id = self._get_collection_id()
            logger.info(f"Коллекция {self.collection_name} создана (UUID: {self.collection_id})")
                
        except Exception as e:
            logger.error(f"Ошибка при проверке/создании коллекции: {str(e)}", exc_info=True)
            raise

    def get_relevant_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Получает релевантный контекст для запроса через HTTP API
        """
        try:
            logger.info(f"Получаем контекст для запроса: {query}")
            # Получаем эмбеддинг запроса
            query_embedding = self.model.encode(query).tolist()
            logger.info("Эмбеддинг запроса получен")
            
            # Формируем запрос к API используя UUID коллекции
            logger.info(f"Отправляем запрос к ChromaDB: {self.base_url}/collections/{self.collection_id}/query")
            response = self.client.post(
                f"{self.base_url}/collections/{self.collection_id}/query",
                params={
                    "tenant": "default_tenant",
                    "database": "default_database"
                },
                json={
                    "query_embeddings": [query_embedding],
                    "n_results": n_results,
                    "include": ["documents", "metadatas", "distances"]
                }
            )
            response.raise_for_status()
            results = response.json()
            logger.info("Получен ответ от ChromaDB")
            
            # Форматируем результаты
            contexts = []
            if results.get('documents') and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    contexts.append({
                        'text': results['documents'][0][i],
                        'metadata': results.get('metadatas', [[]])[0][i] if results.get('metadatas') else {},
                        'relevance': 1 - results['distances'][0][i] if results.get('distances') else 0
                    })
                logger.info(f"Найдено {len(contexts)} релевантных контекстов")
            else:
                logger.info("Релевантные контексты не найдены")
            
            return contexts
            
        except Exception as e:
            logger.error(f"Ошибка при получении контекста: {str(e)}", exc_info=True)
            return []

    def format_context_for_prompt(self, contexts: List[Dict[str, Any]]) -> str:
        """
        Форматирует контекст для включения в промпт
        """
        if not contexts:
            return "Контекст не найден в базе знаний."
            
        formatted_context = "Релевантный контекст из базы знаний:\n\n"
        
        for i, ctx in enumerate(contexts, 1):
            formatted_context += f"Фрагмент {i} (релевантность: {ctx['relevance']:.2f}):\n"
            formatted_context += f"Файл: {ctx['metadata'].get('file_path', 'Неизвестно')}\n"
            formatted_context += f"Текст: {ctx['text']}\n\n"
            
        return formatted_context 