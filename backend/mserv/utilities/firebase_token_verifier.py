#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: backend/mserv/utilities/mfirebase_token_verifier.py

from jose import jwt, JWTError, JOSEError
import requests
from typing import Optional, Any
from fastapi import HTTPException
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

class FirebaseTokenVerifier:
	GOOGLE_CERTS_URL: str
	GOOGLE_ISSUER: str

	GOOGLE_CERTS_URL = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
	GOOGLE_ISSUER = "https://securetoken.google.com/[YOUR_PROJECT_ID]"

	def __init__(self, project_id: str):
		self.project_id = project_id
		self.GOOGLE_ISSUER = self.GOOGLE_ISSUER.replace("[YOUR_PROJECT_ID]", project_id)

	def _fetch_google_certs(self) -> dict[str, str]:
		response = requests.get(self.GOOGLE_CERTS_URL)
		response.raise_for_status()
		return response.json()

	def decode_token(self, token: str) -> dict[str, Any]:
		certs = self._fetch_google_certs()

		unverified_header = jwt.get_unverified_header(token)
		kid = unverified_header['kid']
		alg = unverified_header['alg']

		if kid not in certs:
			raise ValueError("Key ID not found in Google certs")

		# Load the certificate
		cert_str = certs[kid].encode("utf-8")
		cert_obj = load_pem_x509_certificate(cert_str, default_backend())

		# Extract the public key
		public_key = cert_obj.public_key()

		decoded_token = jwt.decode(
			token=token,
			key=public_key, # type: ignore[arg-type]
			algorithms=[alg],
			audience=self.project_id,
			issuer=self.GOOGLE_ISSUER
		)
		return decoded_token
	
	def get_user_id(self, token: str) -> Optional[str]:
		decoded_token = self.decode_token(token)
		return decoded_token.get("user_id", None) if decoded_token else None
