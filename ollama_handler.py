from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from ollama import AsyncClient
import asyncio

app = FastAPI()

async def stream_data(content: str):
    message = {'role': 'user', 'content': content}
    async for part in await AsyncClient().chat(model='llama3.1', messages=[message], stream=True):
        yield part['message']['content'].encode('utf-8')  # Send data as bytes

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    content = data.get('content', '')

    return StreamingResponse(stream_data(content), media_type='text/plain')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
