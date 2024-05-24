from fastapi import FastAPI, Request
from typing import List, Dict
from create_chat_completion_response import CreateChatCompletionResponse
import pprint
from fastapi.responses import StreamingResponse
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post(
    "/v1/chat/completions", response_model=CreateChatCompletionResponse
)
async def create_chat_completion(
    request: Request
) -> CreateChatCompletionResponse:
    # Log basic request details
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")

    # Log headers (optional: filter or select specific headers)
    headers = dict(request.headers)
    logger.info(f"Headers: \n{pprint.pformat(headers, sort_dicts=False)}")

    # Read and log the body
    body = await request.json()
    logger.info(f"Body: \n{pprint.pformat(body, sort_dicts=False)}")

    response = CreateChatCompletionResponse()
    response.choices[0].message.content = "Hello I am a mock AI. How are you doing?"
    response.choices[0].finish_reason = "stop"
    # print(response.model_dump_json(indent=2))
    # print(response.model_dump_json())

    streaming = body.get('stream', False)

    if not streaming:
        logger.info(f'not streaming: {pprint.pformat(response)}')
        return response
    else:
        # Generate array of responses for streaming
        responses = CreateChatCompletionResponse.create_stream_responses('Hello I am a mock AI. How are you doing?')

        # Simulate data generation for the response
        async def response_stream():
            for response in responses:
                yield f"data: {response}\n\n"
                await asyncio.sleep(0.005)
            yield '[DONE]'

        return StreamingResponse(response_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
