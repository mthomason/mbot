# /backend/app/api/v1/endpoints/chat.py
# -*- coding: utf-8 -*-

from mserv.utilities.firebase_token_verifier import FirebaseTokenVerifier
from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, Optional, Tuple, Callable, TypeVar, Union, Generator
from uuid import UUID
import os
import openai

# Load the OpenAI API key from the environment variables
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY_MBOT")
if OPENAI_API_KEY is None:
	raise Exception("OpenAI API key not found in environment variables")

# Load the Google Project ID from the environment variables
GOOGLE_PROJECT_ID: str | None = os.getenv("GOOGLE_PROJECT_ID_MBOT")
if GOOGLE_PROJECT_ID is None:
	raise Exception("Google Project ID not found in environment variables")

router = APIRouter()				# Initalize the FastAPI router

openai.api_key = OPENAI_API_KEY		# Set the OpenAI API key

chats: dict[UUID, list[dict[str, str]]] = {}

class ChatMessage(BaseModel):
	message: str

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

@router.post("/chat")
async def chat_endpoint_async(chat_message: ChatMessage,
							  user_id: str = Depends(get_current_user_id)):
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 1024:
		raise HTTPException(status_code=400, detail="Message too long")

	print("Value:", chat_message)
	print("Type:", type(chat_message))
	print("User ID:", user_id)

	async def event_stream():
		try:
			response = await openai.ChatCompletion.acreate(
				model = "gpt-3.5-turbo",
				messages = [
					{"role": "system", "content": "You are a helpful assistant."},
					{"role": "user", "content": chat_message.message},
					],
				stream = True
			)
			async for chunk in response:
				yield f"{str(chunk)}\n\n"

		except Exception as e:
			raise HTTPException(status_code=400, detail=str(e))

	return StreamingResponse(event_stream(), media_type="text/plain")
