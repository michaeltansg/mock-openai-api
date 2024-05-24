from pydantic import BaseModel, Field
import time
import random
import string
from typing import List, Optional

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class Message(BaseModel):
    role: str = 'assistant'
    content: str = ''

class Choice(BaseModel):
    index: int = 0
    message: Message = Field(default_factory=Message, alias='delta')
    logprobs: None = None
    finish_reason: Optional[str] = None

    class Config:
        populate_by_name = True  # Allows using field names on creation

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class CreateChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: 'chatcmpl-' + generate_random_string(30))
    object: str = 'chat.completion'
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = 'fake-model'
    choices: List[Choice] = Field(default_factory=lambda: [Choice()])
    usage: Usage = Field(default_factory=Usage)
    system_fingerprint: Optional[dict] = None

    @classmethod
    def create_stream_responses(cls, content: str):
        instance = cls()  # Create an instance of cls to use instance methods
        responses: List[CreateChatCompletionResponse] = []

        chunks = instance.split_into_random_chunks(content)

        responses.append(instance.first_delta_message())

        for chunk in chunks:
            responses.append(instance.body_delta_message(chunk))

        responses.append(instance.last_delta_message())

        return responses

    def split_into_random_chunks(self, text):
        i = 0
        chunks = []
        while i < len(text):
            size = random.randint(1, 5)  # Random size between 1 and 5 characters
            chunks.append(text[i:i+size])
            i += size
        return chunks

    def first_delta_message(self):
        self.object = 'chat.completion.chunk'
        return self.json(
            by_alias=True, 
            exclude={"usage": True}
        )

    def body_delta_message(self, text: str):
        self.object = 'chat.completion.chunk'
        self.choices[0].message.content = text
        return self.json(
            by_alias=True,
            exclude={"choices": {"__all__": {"message": {"role": True}}}, "usage": True},
        )

    def last_delta_message(self):
        self.object = 'chat.completion.chunk'
        self.choices[0].finish_reason = 'stop'
        return self.json(
            by_alias=True,
            exclude={
                "choices": {"__all__": {"message": {"role": True, "content": True}}},
                "usage": True,
            },
        )
