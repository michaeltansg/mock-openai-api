uvicorn app:app --reload

curl --location 'http://127.0.0.1:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer XXX' \
--header 'Cookie: __cf_bm=uEE4.shRh6ydUizv6_GXLHc5gRHmTPLyphIgdZwO.NA-1716538942-1.0.1.1-5rAUV8MB0qr9OU4qNsJUvjMrDXsaj.XOhtRfRfWMFqxwwWrwRriz0pTfJyUTlDYel3n7HX05p9SO1Df59fNjXA; _cfuvid=bY5eyH_A8K18omXhGDvTCJRe4wxeK4WKry3BYkPl2rQ-1716538942953-0.0.1.1-604800000' \
--data '{
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
    "stream": false
  }'
