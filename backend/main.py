import os
import uuid
from typing import Dict, List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai

# Import Pydantic models for request/response validation
from core.requests import ChatRequest, ErrorResponse

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-preview-04-17"

app = FastAPI(
    title="Fonte API",
    description="AI assistant for proofreading and drafting writing materials",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=GEMINI_API_KEY)

# In-memory storage for chat histories
# In a production app, you would use a database
chats: Dict[str, List[Dict[str, str]]] = {}

@app.get("/")
def ping():
    return {"message": "hello"}

@app.post("/chat", responses={
    200: {"description": "Successfully generated response"},
    400: {"model": ErrorResponse, "description": "Bad request"},
    500: {"model": ErrorResponse, "description": "Server error"}
})
async def chat(request: ChatRequest):
    """ Test with curl in Docker Desktop:
    curl -X POST http://localhost:8000/chat -H
    'Content-Type: application/json' -d '{"message": "Hello, how are you?"}'
    """
    try:
        message = request.message
        chat_id = request.chat_id
        
        # Create a new chat if chat_id is not provided or not found
        if not chat_id or chat_id not in chats:
            chat_id = str(uuid.uuid4())
            chats[chat_id] = []
        
        # Add the new user message to the chat history
        chats[chat_id].append({"role": "user", "message": message})
        
        # Prepare the conversation history for Gemini
        content_parts = []
        for msg in chats[chat_id]:
            if msg["role"] == "user":
                content_parts.append({"role": "user", "parts": [{"text": msg["message"]}]})
            else:
                content_parts.append({"role": "model", "parts": [{"text": msg["message"]}]})
        
        # Generate streaming response
        response = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=content_parts,
        )
        
        # Capture the full assistant response to save to history
        full_response = []
        
        # Streaming generator
        def gemini_stream():
            try:
                for chunk in response:
                    if chunk.text:
                        full_response.append(chunk.text)
                        yield chunk.text
                
                # Save the assistant's response to chat history
                if full_response:
                    complete_response = "".join(full_response)
                    chats[chat_id].append({"role": "model", "message": complete_response})
                    
                    # Also yield the chat_id so the client knows it for future messages
                    yield f"\n\n__CHAT_ID__:{chat_id}"
            except Exception as e:
                yield f"[ERROR] {str(e)}"
        
        return StreamingResponse(gemini_stream(), media_type="text/plain")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Server error: {str(e)}"})