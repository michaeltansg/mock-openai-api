from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List<Message]
    stream: Optional[bool] = False

class MessageResponse(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: MessageResponse
    logprobs: Optional[Dict] = None
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: str

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def create_completion(
    request: Request,
    authorization: str = Header(None),
    cookie: str = Header(None)
):
    if authorization != "Bearer xxxxx":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    chat_request = await request.json()

    response = ChatResponse(
        id="chatcmpl-9SKkDA18Aiy8ajfSlsXLpI3gO53sJ",
        object="chat.completion",
        created=1716539953,
        model="gpt-4o-2024-05-13",
        choices=[
            Choice(
                index=0,
                message=MessageResponse(
                    role="assistant",
                    content="Hi there! How can I assist you today?"
                ),
                logprobs=None,
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=19,
            completion_tokens=10,
            total_tokens=29
        ),
        system_fingerprint="fp_729ea513f7"
    )
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
