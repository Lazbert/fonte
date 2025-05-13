from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str
    # Add more fields as needed for your LLM requests

@app.get("/")
def ping():
    return {"message": "hello"}

@app.post("/llm")
def generate_response(request: LLMRequest) -> Any:
    pass
