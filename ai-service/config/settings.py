from pydantic_settings import BaseSettings, SettingsConfigDict 
from pydantic import BaseModel
from typing import Any
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Настройки LLM
    LLM_PROVIDER: str
    YANDEX_OAUTH: str
    YANDEX_GET_TOKEN_URL: str
    YANDEX_LLM_URL: str
    YANDEX_CATALOG_ID: str
    YANDEX_API_KEY: str

    # Настройки ChromaDB
    CHROMA_HOST: str = "chroma-db"  # имя сервиса в Docker-сети
    CHROMA_PORT: str = "8000"       # порт по умолчанию
    CHROMA_TENANT: str = "default_tenant"
    CHROMA_DATABASE: str = "default_database"

# from pydantic import BaseModel
# from pydantic_settings import BaseSettings
# from functools import lru_cache
# import os

# class Settings(BaseSettings):
#     llm_provider: str = os.getenv("LLM_PROVIDER")
#     llm_base_url: str = os.getenv("YANDEX_GPT_URL")
#     llm_api_key: str = os.getenv("YANDEX_GPT_URL")
#     catalog: str = os.getenv("YANDEX_CATALOG_ID")

# # @lru_cache
@lru_cache
def get_settings():
    return Settings()