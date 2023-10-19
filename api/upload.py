from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from classes import Pulze, DeepGram, Labs11
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:80001",
    "http://127.0.0.1:8001/upload",
    "http://127.0.0.1:8001/parse",
    "http://127.0.0.1:8001/generate"
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
    try:
        async with aiofiles.open(TARGET_FILENAME, "wb") as buffer:
            await buffer.write(await file.read())
        filename = f"received_{file.filename}"
        if not filename.endswith(".mp3"):
            raise ValueError("The file is not an .mp3")
        return {"filename": filename, "success": True}
    except ValueError as v_err:
        return JSONResponse(status_code=400, content={"detail": str(v_err)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": f"Error saving file: {e}"})
