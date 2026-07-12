from fastapi import FastAPI
from main import repository

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}