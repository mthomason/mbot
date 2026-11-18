import json

import pytest
from pydantic import ValidationError

from mserv.mbot_config import MBotConfig


def config_data():
	return {
		"name": "mbotserver",
		"version": "1.0.0.0",
		"description": "A simple chatbot server for the mbot project.",
		"emojid": "💬🤖",
		"appconfig": {
			"debug": True,
			"log_level": "info",
			"connection_settings": {
				"allow_origins": ["http://localhost:5173"]
			}
		}
	}


def test_loads_the_backend_config():
	config = MBotConfig.load("config.json")

	assert config.name == "mbotserver"
	assert config.version == "1.0.0.0"
	assert "http://localhost:5173" in config.appconfig.connection_settings.allow_origins


def test_missing_config_file():
	with pytest.raises(FileNotFoundError):
		MBotConfig.load("does-not-exist.json")


def test_malformed_config_file(tmp_path):
	path = tmp_path / "bad.json"
	path.write_text("{")

	with pytest.raises(ValueError, match="Failed to decode JSON"):
		MBotConfig.load(str(path))


def test_round_trips_through_unload():
	config = MBotConfig.load("config.json")

	assert config.unload()["name"] == config.name


def test_rejects_an_unknown_log_level():
	data = config_data()
	data["appconfig"]["log_level"] = "verbose"

	with pytest.raises(ValidationError):
		MBotConfig(**data)


def test_rejects_missing_required_fields():
	with pytest.raises(ValidationError):
		MBotConfig(**{"name": "only-a-name"})


def test_config_file_is_valid_json():
	with open("config.json") as config_file:
		assert isinstance(json.load(config_file), dict)
