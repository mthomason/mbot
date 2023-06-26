# /backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import chat

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],  # replace with your frontend's address
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(router=chat.router, prefix="/app/api/v1/endpoints")

@app.get("/")
def read_root():
	return {"Hello": "World"}

