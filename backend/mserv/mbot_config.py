#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: mserv/mbot_config.py

import json
from typing import List
from pydantic import BaseModel, validator

class MBotConfig(BaseModel):

	class ApplicationConfig(BaseModel):

		class ConnectionSettings(BaseModel):
			allow_origins: List[str]

		@validator('log_level')
		def validate_log_level(cls, v):
			allowed_values = ["debug", "info", "warning", "error", "critical"]
			if v not in allowed_values:
				raise ValueError(f"log_level must be one of {allowed_values}")
			return v

		debug: bool
		log_level: str
		connection_settings: ConnectionSettings

	name: str
	version: str
	description: str
	emojid: str
	appconfig: ApplicationConfig

	@classmethod
	def load(cls, file_path: str) -> 'MBotConfig':
		with open(file_path, 'r') as file:
			config_dict = json.load(file)
		return cls(**config_dict)

	def unload(self) -> dict:
		return self.model_dump()
