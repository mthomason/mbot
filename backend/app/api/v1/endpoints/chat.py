# /backend/app/api/v1/endpoints/chat.py
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, Optional, Tuple, Callable, TypeVar, Union, Generator
from uuid import UUID

from mserv.utilities.firebase_token_verifier import FirebaseTokenVerifier

import time
import os
import openai

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY_MBOT")
if OPENAI_API_KEY is None:
	raise Exception("OpenAI API key not found in environment variables")

GOOGLE_PROJECT_ID: str | None = os.getenv("GOOGLE_PROJECT_ID_MBOT")
if GOOGLE_PROJECT_ID is None:
	raise Exception("Google Project ID not found in environment variables")

# Initalize the FastAPI router
router = APIRouter()

# Initialize the OpenAI API
openai.api_key = OPENAI_API_KEY

chats: dict[UUID, list[dict[str, str]]] = {}

# Initialize the Firebase token verifier
def get_verifier(project_id: str = GOOGLE_PROJECT_ID):
	return FirebaseTokenVerifier(project_id)

async def get_current_user_id(request: Request, verifier: FirebaseTokenVerifier = Depends(get_verifier)) -> str:
	# Extract the token from the Authorization header
	token = request.headers.get('Authorization')
	if not token:
		raise HTTPException(status_code=401, detail="Token is missing")
	
	# Remove the Bearer prefix if it exists
	token = token.replace("Bearer ", "")
	
	# Use the verifier to extract the user ID from the token
	user_id = verifier.get_user_id(token)
	
	if user_id is None:
		raise HTTPException(status_code=401, detail="User not authenticated")
	
	return user_id

class ChatMessage(BaseModel):
	message: str

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
