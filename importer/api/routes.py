from fastapi import APIRouter, Depends
from loader import parse_directory
from schemas import ImportRequest


router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}
#response_model=QueryResponse
@router.post("/imports")
def imports(request: ImportRequest):
    print("Import started!", request.path)
    parse_directory(request.path)
    return {"status": "success"}