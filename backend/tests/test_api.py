import asyncio
import json
from types import SimpleNamespace

import main
from app.api.v1.endpoints import chat


def test_health(client):
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_ping(client):
	response = client.get("/ping")

	assert response.status_code == 200
	assert response.json() == {"ping": "pong"}


def test_root_returns_config_metadata(client):
	response = client.get("/")

	assert response.status_code == 200
	assert response.json() == {"app": main.mbotconfig.emojid}


def test_name_and_version(client):
	assert client.get("/name").json() == {"name": main.mbotconfig.name}
	assert client.get("/version").json() == {"version": main.mbotconfig.version}


def test_chat_requires_authentication(client):
	response = client.post("/chat", json={"message": "hello"})

	assert response.status_code == 401


def test_chat_returns_401_when_token_verification_fails(client, monkeypatch):
	def raise_verification_error(self, token):
		raise ValueError("bad token")

	monkeypatch.setattr(chat.FirebaseTokenVerifier, "get_user_id", raise_verification_error)

	response = client.post(
		"/chat",
		json={"message": "hello"},
		headers={"Authorization": "Bearer invalid"}
	)

	assert response.status_code == 401


def test_chat_rejects_empty_message(authed_client):
	response = authed_client.post("/chat", json={"message": ""})

	assert response.status_code == 400
	assert response.json()["detail"] == "Empty message provided"


def test_chat_rejects_oversized_message(authed_client):
	response = authed_client.post("/chat", json={"message": "x" * 1025})

	assert response.status_code == 400
	assert response.json()["detail"] == "Message too long"


def test_chat_streams_ndjson(authed_client, monkeypatch):
	class Chunk:
		def __init__(self, content, finish_reason=None):
			self.choices = [
				SimpleNamespace(
					delta=SimpleNamespace(content=content),
					finish_reason=finish_reason
				)
			]

	async def fake_response(message):
		async def generate():
			yield Chunk("Hello")
			yield Chunk(" world", "stop")

		return generate()

	monkeypatch.setattr(chat, "get_chat_response_async", fake_response)

	response = authed_client.post("/chat", json={"message": "hi"})

	assert response.status_code == 200
	assert response.headers["content-type"].startswith("application/x-ndjson")

	events = [json.loads(line) for line in response.text.strip().splitlines()]
	assert [event["content"] for event in events] == ["Hello", " world"]
	assert events[-1]["is_end"] is True
	assert all(event["user_id"] == "test-user" for event in events)


def test_openai_request_uses_configured_model(monkeypatch):
	captured = {}

	class FakeCompletions:
		async def create(self, **kwargs):
			captured.update(kwargs)
			return "fake-stream"

	fake_client = SimpleNamespace(
		chat=SimpleNamespace(completions=FakeCompletions())
	)
	monkeypatch.setattr(chat, "async_openai_client", fake_client)

	result = asyncio.run(chat.get_chat_response_async("hi"))

	assert result == "fake-stream"
	assert captured["model"] == "test-model"
	assert captured["stream"] is True
	assert captured["messages"][-1] == {"role": "user", "content": "hi"}
	assert captured["messages"][0]["role"] == "system"
