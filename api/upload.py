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

TARGET_FILENAME = "TARGET_AUDIO.mp3"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file and saves it as the Target Audio file we want to process. Can call in javascript with the following
    lines:

    const formData = new FormData();
    formData.append('file', file);
    fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData })
    """
    try:
        file_contents = await file.read()
        filename = f"received_{file.filename}"

        if not filename.endswith(".mp3"):
            raise ValueError("The file is not an .mp3")

        with open(TARGET_FILENAME, "wb") as buffer:
            buffer.write(file_contents)

        return {"filename": filename, "success": True}
    except ValueError as v_err:
        return JSONResponse(status_code=400, content={"detail": str(v_err)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": f"Error saving file: {e}"})
