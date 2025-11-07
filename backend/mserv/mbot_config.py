#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: backend/mserv/mbot_config.py

import json
from pydantic import BaseModel, validator, Field
from typing import List

class MBotConfig(BaseModel):

	class ApplicationConfig(BaseModel):

		class ConnectionSettings(BaseModel):
			allow_origins: List[str] = Field(default_factory=list)

		@validator('log_level', pre=True, always=True)
		def validate_log_level(cls, v):
			allowed_values = ["debug", "info", "warning", "error", "critical"]
			if v not in allowed_values:
				raise ValueError(f"log_level must be one of {allowed_values}")
			return v

		debug: bool
		log_level: str
		connection_settings: ConnectionSettings = Field(default_factory=ConnectionSettings)

	name: str
	version: str
	description: str
	emojid: str
	appconfig: ApplicationConfig

	@classmethod
	def load(cls, file_path: str) -> 'MBotConfig':
		try:
			with open(file_path, 'r') as file:
				config_dict = json.load(file)
				return cls(**config_dict)
		except FileNotFoundError:
			raise FileNotFoundError(f"The configuration file {file_path} does not exist.")
		except json.JSONDecodeError as e:
			raise ValueError(f"Failed to decode JSON from {file_path}: {e}")

	def unload(self) -> dict:
		return self.model_dump()

type FastApiConnSettings = MBotConfig.ApplicationConfig.ConnectionSettings
