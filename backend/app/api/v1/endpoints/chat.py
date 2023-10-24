# /backend/app/api/v1/endpoints/chat.py
# -*- coding: utf-8 -*-

import asyncio
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator, Any, Optional, Tuple, Callable, TypeVar, Union, Generator
from uuid import UUID
import os
import openai
from openai.types.chat import ChatCompletionChunk

from mserv.utilities.firebase_token_verifier import FirebaseTokenVerifier

OPENAI_PREVIEW: bool = True

# Load the OpenAI API key from the environment variables
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY_MBOT")
if OPENAI_API_KEY is None:
	raise Exception("OpenAI API key not found in environment variables")

# Load the Google Project ID from the environment variables
GOOGLE_PROJECT_ID: str | None = os.getenv("GOOGLE_PROJECT_ID_MBOT")
if GOOGLE_PROJECT_ID is None:
	raise Exception("Google Project ID not found in environment variables")

router: APIRouter = APIRouter()			# Initalize the FastAPI router
async_openai_client: openai.AsyncOpenAI  = openai.AsyncClient(api_key=OPENAI_API_KEY)	# Initialize the OpenAI client

chats: dict[UUID, list[dict[str, str]]] = {}

class ChatMessage(BaseModel):
	message: str

class ChatResponse(BaseModel):
	user_id: str
	content: str
	is_end: bool

async def get_chat_response_async(message: str) -> openai.AsyncStream[ChatCompletionChunk] | None:
	return await async_openai_client.chat.completions.create(
					model = "gpt-3.5-turbo",
					messages = [
						{"role": "system", "content": "You are a helpful assistant."},
						{"role": "user", "content": message},
						],
					stream = True
				)

async def get_chat_response_async_legacy(message: str) -> Any:
	return await openai.ChatCompletion.acreate(
					model = "gpt-3.5-turbo",
					messages = [
						{"role": "system", "content": "You are a helpful assistant."},
						{"role": "user", "content": message},
						],
					stream = True
				)

# Get the current user ID from the request
async def get_current_user_id(request: Request) -> str:
	auth_token: str = request.headers.get('Authorization')
	if not auth_token:
		raise HTTPException(status_code=401, detail="Token is missing")

	auth_token = auth_token.replace("Bearer ", "")

	verifier: FirebaseTokenVerifier = FirebaseTokenVerifier(GOOGLE_PROJECT_ID)
	user_id: str = verifier.get_user_id(auth_token)

	if user_id is None:
		raise HTTPException(status_code=401, detail="User not authenticated")

	return user_id

@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat_endpoint_async(chat_message: ChatMessage,
							  user_id: str = Depends(get_current_user_id)) -> StreamingResponse:
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 1024:
		raise HTTPException(status_code=400, detail="Message too long")

	print("Value:", chat_message)
	print("Type:", type(chat_message))
	print("User ID:", user_id)

	async def event_stream_json_async() -> AsyncGenerator[str, None]:
		try:
			response: ChatCompletionChunk | None = await get_chat_response_async(chat_message.message)
			is_end: bool = False
			async for chunk in response:
				is_end = chunk.choices[0].finish_reason == "stop"
				if is_end:
					break
				content: str = chunk.choices[0].delta.content
				yield ChatResponse(user_id=user_id, content=content, is_end=is_end).model_dump_json() + "\n"
		except Exception as e:
			raise HTTPException(status_code=400, detail=str(e))

	async def event_stream_text_async():
		try:
			response: ChatCompletionChunk | None = await get_chat_response_async(chat_message.message)
			the_end: bool = False
			async for chunk in response:
				content: str = chunk.choices[0].delta.content
				if content is not None:
					yield f"{str(content)}\n\n"
				else:
					yield f"{str()}\n\n"

		except Exception as e:
			raise HTTPException(status_code=400, detail=str(e))

	return StreamingResponse(event_stream_json_async(), media_type="application/x-ndjson")
