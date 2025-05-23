from fastapi import APIRouter, Depends, HTTPException
from config.settings import get_settings
from schemas import QueryRequest, QueryResponse
# from llm.client import get_llm_client
from llm.client import Client
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}
#response_model=QueryResponse
@router.post("/query")
def query(req: QueryRequest, settings=Depends(get_settings)):
    try:
        logger.info(f"Получен запрос: {req.prompt}")
        logger.info(f"Настройки ChromaDB: host={settings.CHROMA_HOST}, port={settings.CHROMA_PORT}")
        
        client = Client(settings)
        logger.info("Клиент LLM инициализирован")
        
        result = client.query(req.prompt)
        logger.info("Запрос успешно обработан")
        
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))