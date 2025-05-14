from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    prompt: str


class Message(BaseModel):
    role: str
    text: str

class Alternative(BaseModel):
    message: Message
    status: str

class UsageDetails(BaseModel):
    reasoning_tokens: int = 0 

class Usage(BaseModel):
    input_text_tokens: str
    completion_tokens: str
    total_tokens: str
    completion_tokens_details: UsageDetails

# class Result(BaseModel):
#     alternatives: List[Alternative]
#     usage: Usage
#     model_version: str 

class QueryResponse(BaseModel): 
    body: str
    model_version: str
    input_text_tokens: str
    completion_tokens: str
    total_tokens: str