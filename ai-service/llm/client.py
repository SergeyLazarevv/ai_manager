from config.settings import Settings
from llm.base import BaseLLMClient
import httpx
from dotenv import find_dotenv, load_dotenv
import os
from functools import lru_cache
from dto.yandex_llm_request import YandexGPTRequest
from cachetools import TTLCache
import time
from .vector_store import VectorStore

class Client(BaseLLMClient):
    def __init__(self, settings: Settings):
        self.url = settings.YANDEX_LLM_URL
        self.auth = TTLCache(maxsize=1, ttl=3600)
        load_dotenv()
        self.oauth_token = os.getenv('YANDEX_OAUTH')
        self.token_url = os.getenv('YANDEX_GET_TOKEN_URL')
        self.vector_store = VectorStore()

    def get_token(self):
        if "token" in self.auth:
            return self.auth["token"]
        
        # Запрашиваем новый токен
        new_token = self.fetch_new_token()
        self.auth["token"] = new_token
        return new_token

    def fetch_new_token(self):
        print("Получаем новый токен...")
        try:
            response = httpx.post(
                url=self.token_url,
                headers={'Content-Type': 'application/json'},
                json={'yandexPassportOauthToken': self.oauth_token},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if 'iamToken' in data:
                print("Success: Token получен")
                return data['iamToken']
            else:
                print(f"Error: {data}")
                raise Exception(f"Failed to get token: {data}")
                
        except Exception as e:
            print(f"Error getting token: {str(e)}")
            raise

    def query(self, prompt: str) -> str:
        print('in query method')
        
        # Получаем релевантный контекст
        contexts = self.vector_store.get_relevant_context(prompt)
        formatted_context = self.vector_store.format_context_for_prompt(contexts)
        
        # Формируем расширенный промпт с контекстом
        enhanced_prompt = f"""Используя предоставленный контекст, ответь на вопрос.

{formatted_context}

Вопрос: {prompt}

Ответ должен быть основан на предоставленном контексте. Если в контексте нет информации для ответа, так и укажи."""

        request_data = YandexGPTRequest(enhanced_prompt).to_dict()
        print('request_data', request_data)

        response = httpx.post(
            url=self.url,
            headers={
                "Authorization": f"Bearer {self.get_token()}",
                "Content-Type": "application/json"
            },
            json={
                **request_data,
                "max_tokens": 2000
            },
            timeout=60.0
        )
        response.raise_for_status()
        response = response.json()

        return {
            "body": response['result']['alternatives'][0]['message']['text'],
            "model_version": response['result']['modelVersion'],
            "input_text_tokens": response['result']['usage']['inputTextTokens'],
            "completion_tokens": response['result']['usage']['completionTokens'],
            "total_tokens": response['result']['usage']['totalTokens'],
        }

# def get_llm_client(provider: str, settings: Settings) -> BaseLLMClient:
#     print(12121212)
#     print(provider)
#     print(3434343434)
#     print(os.getenv("LLM_PROVIDER"))
#     if provider == "yandex":
#         return Client(settings)
#     raise ValueError(f"Unknown LLM provider: {provider}")