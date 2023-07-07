#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import chat

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:5173",
		"http://localhost:8080",
		"http://127.0.0.1",
		"http://localhost"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(chat.router)

@app.get("/")
def read_root():
	return {"Hello": "World"}

