import io
from typing import List
import ollama
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

MODEL = "phi3:medium-128k"

app = FastAPI()


class PromptRequest(BaseModel):
    role: str
    prompt: str


@app.get("/")
async def root():
    return FileResponse("copilot_api/index.html")


@app.post("/generate")
async def generate_response(request: List[PromptRequest]) -> StreamingResponse:
    print()
    print(f"Received message: {request[-1].prompt}")
    try:
        messages = []
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful assistant call Pi ready to help with any task. You are happy and enthusiastic, but your answers are short and to the point.",
            }
        )

        for p in request:
            messages.append({"role": p.role, "content": p.prompt})

        stream = ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        async def llm_streamer(llm_stream):
            for chunk in llm_stream:
                print(chunk["message"]["content"], end="")
                # print the type of chunk

                yield chunk["message"]["content"]

        return StreamingResponse(llm_streamer(stream), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    print("Hello World")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("copilot_api.main:app", host="0.0.0.0", port=8000, reload=True)
