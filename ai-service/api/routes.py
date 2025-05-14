from fastapi import APIRouter, Depends, HTTPException
from config.settings import get_settings
from schemas import QueryRequest, QueryResponse
# from llm.client import get_llm_client
from llm.client import Client

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}
#response_model=QueryResponse
@router.post("/query")
def query(req: QueryRequest, settings=Depends(get_settings)):
    print('start in router')
    client = Client(settings)
    try:
        result =client.query(req.prompt)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))