#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: main.py

from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import json
from app.api.v1.endpoints import chat
from mserv.mbot_config import MBotConfig

app: FastAPI = FastAPI()
mbotconfig: MBotConfig = MBotConfig.load("config.json")

app.add_middleware(
	CORSMiddleware,
	allow_origins=mbotconfig.appconfig.connection_settings.allow_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(chat.router)

@app.get("/")
def read_root() -> dict[str, str]:
	return {
		"app": mbotconfig.emojid,
		}

@app.get("/name")
def name() -> dict[str, str]:
	return {"name": mbotconfig.name}

@app.get("/version")
def version() -> dict[str, str]:
	return {"version": mbotconfig.version}

@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}

@app.get("/ping")
def ping() -> dict[str, str]:
	return {"ping": "pong"}
