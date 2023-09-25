# /backend/app/api/v1/endpoints/chat.py
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import time
from typing import Any, Optional, Tuple, Callable, TypeVar, Union, Generator
from uuid import UUID

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY_MBOT")

router = APIRouter()

chats: dict[UUID, list[dict[str, str]]] = {}

class ChatMessage(BaseModel):
	message: str

@router.post("/chat")
async def chat_endpoint_async(chat_message: ChatMessage):
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 1024:
		raise HTTPException(status_code=400, detail="Message too long")

	print("Value:", chat_message)
	print("Type:", type(chat_message))

	try:
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": chat_message.message},
				],
			stream=True
		)

		async def event_stream():
			for chunk in response:
				yield f"{str(chunk)}\n\n"

		return StreamingResponse(event_stream(), media_type="text/plain")

	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
