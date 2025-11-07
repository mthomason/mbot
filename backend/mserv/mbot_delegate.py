#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: mserv/mbot_delegate.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from mserv.mbot_config import MBotConfig

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

	@asynccontextmanager
	async def lifespan(self, app: FastAPI):
		print("App Startup Events")
		yield
		print("App Shutdown Events")

	def is_initalized(self) -> bool:
		return self._is_initialized

	def unload(self) -> dict:
		self.fastapi_app = None
		return self.mbotconfig.unload()
