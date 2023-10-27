#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: mserv/mbot_delegate.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from mserv.mbot_config import MBotConfig

import aioboto3


class DynamoDBHelper:
	def __init__(self, db_settings: MBotConfig.ApplicationConfig.DatabaseSettings.DynamoDBSettings):
		self._dynamodb_params = {
			"region_name": db_settings.region_name,
			"endpoint_url": db_settings.endpoint_url,
		}

	async def get_dynamodb(self):
		return await self.get_dynamodb_resource()

	async def get_dynamodb_resource(self):
		return await aioboto3.resource("dynamodb", **(self._dynamodb_params))

	async def get_dynamodb_client(self):
		return await aioboto3.client("dynamodb", **(self._dynamodb_params))

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
	_is_loaded: bool = False
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

		# One time initialization goes here
		#lifespan = self.lifespan
		#self.mbotconfig = MBotConfig.load("config.json")
		#self.fastapi_app = FastAPI(lifespan=lifespan)

		self._is_initialized = True # now initialized
		return

	def load(self) -> bool:
		if self._is_loaded:
			return True
		self._is_loaded = True
		lifespan = self.lifespan
		self.mbotconfig = MBotConfig.load("config.json")
		self.fastapi_app = FastAPI(lifespan=lifespan)
		return True

	async def load_async(self) -> bool:
		if self._is_loaded:
			return True
		self._is_loaded = True
		lifespan = self.lifespan
		self.mbotconfig = await MBotConfig.load_async("config.json")
		self.fastapi_app = FastAPI(lifespan=lifespan)
		return True

	@asynccontextmanager
	async def lifespan(self, app: FastAPI):
		db_settings: MBotConfig.ApplicationConfig.DatabaseSettings.DynamoDBSettings
		db_settings = self.mbotconfig.appconfig.database_settings.dynamodb

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

	# Create tables if they do not exist.
	#async def create_tables_async(self) -> bool:
	#	dynamodb = await self.get_dynamodb()

	#	async with dynamodb.Table("users").batch_writer() as batch:
	#		await batch.put_item(Item={
	#			"userid": "1234567890",
	#			"username": "testuser",
	#			"email": "",
	#			"password": "",
	#			"created": "",
	#			"updated": "",
	#			})
	#	return True
