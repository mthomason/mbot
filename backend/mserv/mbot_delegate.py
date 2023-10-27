#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: mserv/mbot_delegate.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from mserv.mbot_config import MBotConfig


class DynamoDBHelper:
	async def exists(self, table_name) -> bool:
		result: bool = False
		#try:
			#client = aioboto3.client("dynamodb", **(self._dynamodb_params))
			#await client.describe_table(TableName=table_name)
		#	result = True
		#except ClientError as err:
		#	result = False
		#return result

class MbotDelegate:
	_instance = None
	_lock = threading.Lock()  # Protects '_instance' during its first assignment
	_is_initialized: bool = False
	_dynamodb_params: dict[str, str]
	fastapi_app: FastAPI
	mbotconfig: MBotConfig

	def __new__(cls, *args, **kwargs):
		with cls._lock:
			if not cls._instance:
				cls._instance = super(MbotDelegate, cls).__new__(cls)
				cls._is_initialized = False  # init is called after new
		return cls._instance

	def __init__(self):
		if self._is_initialized:
			return

		self.fastapi_app = FastAPI(lifespan=MbotDelegate.lifespan)
		mbotconfig: MBotConfig = MBotConfig.load("config.json")
		dynamondb_settings: MBotConfig.ApplicationConfig.DatabaseSettings.DynamoDBSettings
		dynamondb_settings = mbotconfig.appconfig.database_settings.dynamodb
		self._dynamodb_params = {
			"region_name": dynamondb_settings.region_name,
			"endpoint_url": dynamondb_settings.endpoint_url,
		}
		self.mbotconfig = mbotconfig

		self._is_initialized = True # now initialized
		return

	@asynccontextmanager
	async def lifespan(app: FastAPI):
		print("App Startup Events")

		yield
		print("App Shutdown Events")


	def db_settings(self) -> MBotConfig.ApplicationConfig.DatabaseSettings:
		return self.mbotconfig.appconfig.database_settings

	def is_initalized(self) -> bool:
		return self._is_initialized

	def unload(self) -> dict:
		self.fastapi_app = None
		return self.mbotconfig.unload()
