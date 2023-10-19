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

@app.get("/")
def root():
    return {"status": "Crux API Active!"}
