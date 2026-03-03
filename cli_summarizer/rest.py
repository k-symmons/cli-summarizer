from enum import Enum
from fastapi import FastAPI, Request
from .llm import summarize, Length

app = FastAPI()



@app.post("/")
def summarize_text(text: str, length: Length):
    return summarize(text,length)
