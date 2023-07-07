# /backend/app/api/v1/endpoints/chat.py

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from typing import Any, Optional, Tuple, Callable, TypeVar, Union
from uuid import UUID

import os

import openai
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY_MBOT")

router = APIRouter()

chats: dict[UUID, list[dict[str, str]]] = {}

class ChatMessage(BaseModel):
	message: str

# Define a helper function for validation
def validate_message(chat_message: ChatMessage):
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 256:
		raise HTTPException(status_code=400, detail="Message too long")

@router.post("/chat")
async def chat_endpoint_async(chat_message: ChatMessage):
	validate_message(chat_message)

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
			#i: int = 0
			for chunk in response:
				#print(f"Chunk {i}: `{chunk}`")
				yield str(chunk).join(("\n", "\n"))
				#i += 1

		return StreamingResponse(event_stream())

	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
