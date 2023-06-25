# /backend/app/api/v1/endpoints/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY_MBOT")

router = APIRouter()

class ChatMessage(BaseModel):
	message: str

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
	response = openai.ChatCompletion.create(
		model="gpt-4", # Replace with the model you want to use
		messages=[
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": chat_message.message},
		]
	)

	if response is None:
		raise HTTPException(status_code=400, detail="Unable to process the message")

	return {"response": response.choices[0].message['content']}
