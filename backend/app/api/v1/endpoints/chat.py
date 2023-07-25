# /backend/app/api/v1/endpoints/chat.py
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from typing import Any, Optional, Tuple, Callable, TypeVar, Union
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

		# Since FastAPI doesn't support Server-Sent Events (SSE) natively,
		# we'll convert the response to a string and yield each chunk as it arrives.
		async def event_stream():
			#yield "["
			for chunk in response:
				#print("Value: ", chunk)
				#print("Type: ", type(chunk))
				#yield str(chunk).join(("", ","))
				yield str(chunk).join(("\n", "\n"))

			#yield "]"

		return StreamingResponse(event_stream())

	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
