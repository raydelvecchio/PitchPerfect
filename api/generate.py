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

class RequestData(BaseModel):
    username: str
    script: str

@app.post("/generate")
def get_mp3(data: RequestData):
    """
    Given a username and a script, generate a new .mp3 in the style of the TARGET_FILE, or the originally uploaded
    reference clip. Then, send that file back to the frontend for a user to listen to or download.
    """
    if data.username is None:
        raise HTTPException(status_code=400, detail="username parameter required!")
    if data.script is None:
        raise HTTPException(status_code=400, detail="script parameter required!")

    lab = Labs11(data.username)
    location = lab.generate_custom_response(TARGET_FILENAME, data.script)

    return FileResponse(location, media_type="audio/mpeg",
                        headers={"Content-Disposition": f"attachment; filename=simulation.mp3"})