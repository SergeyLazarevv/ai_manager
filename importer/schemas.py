from pydantic import BaseModel

class ImportRequest(BaseModel):
    path: str