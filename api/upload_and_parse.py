from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .classes import Pulze, DeepGram, Labs11
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:80001",
    "http://127.0.0.1:8001/upload",
    "http://127.0.0.1:8001/parse",
    "http://127.0.0.1:8001/generate",    
    "https://crux-be.vercel.app",
    "https://crux-be.vercel.app/upload",
    "https://crux-be.vercel.app/parse",
    "https://crux-be.vercel.app/generate"    
    "https://crux-frontend-nine.vercel.app",
    "https://crux-frontend-nine.vercel.app/upload",
    "https://crux-frontend-nine.vercel.app/parse",
    "https://crux-frontend-nine.vercel.app/generate"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

pulze = Pulze()
deep = DeepGram()
TARGET_FILENAME = "TARGET_AUDIO.mp3"

class RequestData(BaseModel):
    file: UploadFile = File(...)
    audience: str = 'everyone'


@app.post("/upload_and_parse")
async def upload_and_parse(data: RequestData):
    """
    Given an input audience, using the received file buffer, generate feedback and write a new script, then
    return them. Can call in javascript with the following
    lines:

    const formData = new FormData();
    formData.append('file', file);
    formData.append('audience', audience);

    fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData })


    """

    # if data.audience is None:
    #     raise HTTPException(status_code=400, detail="audience parameter required!")

    # if data.file is None:
    #     raise HTTPException(status_code=400, detail="no audio file received!")
    
    try:
        file_contents = await data.file.read()
        filename = f"received_{data.file.filename}"

        with open(TARGET_FILENAME, "wb") as buffer:
            buffer.write(file_contents)

        transcription, length = deep.transcribe(TARGET_FILENAME)
        pulze.configure_initial_prompts(data.audience)
        feedback, new_script = pulze.generate_feedback(transcription, length)
        pulze.reset_context()  # this is NECESSARY to avoid messing up context window of pulze LLMs

        return {"filename": filename, "feedback": feedback, "newScript": new_script}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the audience input: {e}")
