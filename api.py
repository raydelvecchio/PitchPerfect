from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from classes import Pulze, DeepGram, Labs11
from pydantic import BaseModel
import uvicorn


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8001/upload",
    "http://127.0.0.1:8001/parse",
    "http://127.0.0.1:8001/generate",
    "http://localhost:3000",
    "http://localhost:3000/upload",
    "http://localhost:3000/parse",
    "http://localhost:3000/generate",
    "https://quacrobat.pythonanywhere.com",
    "https://quacrobat.pythonanywhere.com/upload",
    "https://quacrobat.pythonanywhere.com/parse",
    "https://quacrobat.pythonanywhere.com/generate"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pulze = Pulze()
deep = DeepGram()
TARGET_FILENAME = "TARGET_AUDIO.mp3"


class RequestData(BaseModel):
    username: str
    script: str


@app.get("/")
def root():
    return {"status": "Crux API Active!"}


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
