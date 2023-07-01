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

#@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
	validate_message(chat_message)

	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": chat_message.message},
		]
	)

	if response is None:
		raise HTTPException(status_code=400, detail="Unable to process the message")

	return {"response": response.choices[0].message['content']}

@router.post("/chat")
async def achat_endpoint(chat_message: ChatMessage):
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
			for chunk in response:
				yield str(chunk).join(("\n", "\n"))

		return StreamingResponse(event_stream())

	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

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

		async def extract_response():
			for chunk in response:
				first_choice = chunk['choices'][0]
				#print(chunk)
				yield {
					'created': chunk['created'],
					'index': first_choice['index'],
					'role': first_choice['delta']['role'],
					'message': first_choice['delta']['content'],  # Assume the message is in this location
					'finish_reason' : first_choice['finish_reason'],
				}

		return StreamingResponse(extract_response(), media_type="application/json")
		#return await extract_response()

	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
