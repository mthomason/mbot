# /backend/app/api/v1/endpoints/chat.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY_MBOT")

router = APIRouter()

class ChatMessage(BaseModel):
	message: str

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 256:
		raise HTTPException(status_code=400, detail="Message too long")
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo", # Replace with the model you want to use
		messages=[
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": chat_message.message},
		]
	)

	if response is None:
		raise HTTPException(status_code=400, detail="Unable to process the message")

	return {"response": response.choices[0].message['content']}

@router.post("/achat")
async def achat_endpoint(chat_message: ChatMessage):
	if chat_message.message is None:
		raise HTTPException(status_code=400, detail="No message provided")
	if len(chat_message.message) == 0:
		raise HTTPException(status_code=400, detail="Empty message provided")
	if len(chat_message.message) > 256:
		raise HTTPException(status_code=400, detail="Message too long")

	try:
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", # Replace with the model you want to use
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
				yield str(chunk)
				
		return StreamingResponse(event_stream())
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
