uvicorn app:app --reload
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer xxxx" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ],
    "stream": true
  }'



{
    "id": "chatcmpl-FindQX3pWVbTgFx5hv11UgWNMUS90a",
    "object": "chat.completion.chunk",
    "created": 1716545324,
    "model": "fake-model",
    "choices": [
        {
            "index": 0,
            "delta": {},
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "system_fingerprint": null,
    "citations": [
        {
            "source": "",
            "page": "",
            "metadata": ""
        }
    ]
}