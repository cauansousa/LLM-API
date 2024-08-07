from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import AsyncClient
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    uvicorn.run(app, host="127.0.0.1", port=3000)
