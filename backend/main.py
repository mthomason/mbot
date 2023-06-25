# /backend/main.py

from fastapi import FastAPI
from app.api.v1.endpoints import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def read_root():
	return {"Hello": "World"}

