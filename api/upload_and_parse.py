from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .classes import Pulze, DeepGram, Labs11
from io import BytesIO  # Import BytesIO

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

@app.post("/upload_and_parse")
async def upload_and_parse(audience: str = Form(...), file: UploadFile = File(...)):
    """
    Given an input audience, using the received file buffer, generate feedback and write a new script, then
    return them.
    """
    try:
        file_contents = await file.read()
        audio_buffer = BytesIO(file_contents)

        
        source = {'buffer': audio_buffer, 'mimetype': 'audio/mp3'}  # Assuming the file is an MP3
        transcription, length = deep.transcribe(source)  # Pass the buffer and mimetype to deep.transcribe
        
        print("Transcription:", transcription)
        print("Length:", length)
        print("Audience:", audience)
        pulze.configure_initial_prompts(audience)
        feedback, new_script = pulze.generate_feedback(transcription, length)
        pulze.reset_context()  # Reset context to avoid messing up the context window of pulze LLMs
        
        return {"feedback": feedback, "newScript": new_script}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the audience input: {e}")