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

@app.get("/parse")
def get_info(audience: str):
    """
    Given an input audience, using the saved TARGET_FILENAME, generate feedback and write a new script, then
    return them.
    """
    if audience is None:
        raise HTTPException(status_code=400, detail="audience parameter required!")

    try:
        transcription, length = deep.transcribe(TARGET_FILENAME)
        pulze.configure_initial_prompts(audience)
        feedback, new_script = pulze.generate_feedback(transcription, length)
        pulze.reset_context()  # this is NECESSARY to avoid messing up context window of pulze LLMs

        return {"feedback": feedback, "newScript": new_script}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the audience input: {e}")
