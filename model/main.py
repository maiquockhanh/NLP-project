from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from evaluate import run_eval
from typing import List
from getCorpusFromGG import searchGG
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluatePostData(BaseModel):
    links: List[str]
    query: str

@app.get("/about")
def about():
    return {"Mai Quoc Khanh": "19125024"}

@app.get("/search")
def searchGoogle(q: Optional[str] = None, n: Optional[str] = 5):
    link = searchGG(q, n)
    return link

@app.post("/evaluate")
def evaluate(body: EvaluatePostData):
    return {run_eval(body.links, body.query) }