import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
os.chdir(BACKEND_DIR)
sys.path.insert(0, str(BACKEND_DIR))

# Set these before importing the app: chat.py validates them at import time.
# Use assignment rather than setdefault so a developer's real environment can
# never cause the test suite to call a real provider.
os.environ["OPENAI_API_KEY_MBOT"] = "test-key"
os.environ["GOOGLE_PROJECT_ID_MBOT"] = "test-project"
os.environ["AI_MODEL_CHAT_FAST"] = "test-model"
os.environ["OPENAI_BASE_URL_MBOT"] = "http://127.0.0.1:9/v1"

import pytest
from fastapi.testclient import TestClient

import main
from app.api.v1.endpoints import chat


@pytest.fixture()
def client():
	with TestClient(main.fastapi_app) as test_client:
		yield test_client


@pytest.fixture()
def authed_client():
	main.fastapi_app.dependency_overrides[chat.get_current_user_id] = lambda: "test-user"
	try:
		with TestClient(main.fastapi_app) as test_client:
			yield test_client
	finally:
		main.fastapi_app.dependency_overrides.clear()
