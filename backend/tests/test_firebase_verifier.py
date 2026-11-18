from mserv.utilities.firebase_token_verifier import FirebaseTokenVerifier


def test_issuer_is_scoped_to_the_project():
	verifier = FirebaseTokenVerifier("test-project")

	assert verifier.GOOGLE_ISSUER == "https://securetoken.google.com/test-project"


def test_get_user_id_returns_the_claim(monkeypatch):
	verifier = FirebaseTokenVerifier("test-project")
	monkeypatch.setattr(verifier, "decode_token", lambda token: {"user_id": "user-1"})

	assert verifier.get_user_id("token") == "user-1"


def test_get_user_id_returns_none_without_the_claim(monkeypatch):
	verifier = FirebaseTokenVerifier("test-project")
	monkeypatch.setattr(verifier, "decode_token", lambda token: {"sub": "user-1"})

	assert verifier.get_user_id("token") is None


def test_fetches_google_certificates(monkeypatch):
	class FakeResponse:
		def raise_for_status(self):
			return None

		def json(self):
			return {"kid": "certificate"}

	monkeypatch.setattr(
		"mserv.utilities.firebase_token_verifier.requests.get",
		lambda url: FakeResponse()
	)

	verifier = FirebaseTokenVerifier("test-project")

	assert verifier._fetch_google_certs() == {"kid": "certificate"}
