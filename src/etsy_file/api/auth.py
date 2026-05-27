import hashlib
import json
import secrets
import time
from base64 import urlsafe_b64encode
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlencode

import httpx

ETSY_AUTH_URL = "https://www.etsy.com/oauth/connect"
ETSY_TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"

DEFAULT_SCOPES = [
    "listings_r",
    "listings_w",
    "listings_d",
    "transactions_r",
    "shops_r",
]


@dataclass
class OAuthTokens:
    access_token: str
    refresh_token: str
    expires_at: float  # unix timestamp


class TokenStore:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load(self) -> OAuthTokens | None:
        if not self._path.exists():
            return None
        data = json.loads(self._path.read_text())
        return OAuthTokens(**data)

    def save(self, tokens: OAuthTokens) -> None:
        self._path.write_text(json.dumps(asdict(tokens), indent=2))


class EtsyAuth:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        redirect_uri: str,
        token_file: str,
        scopes: list[str] | None = None,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self._store = TokenStore(token_file)
        self._scopes = scopes or DEFAULT_SCOPES
        self._code_verifier: str | None = None

    def get_auth_url(self) -> tuple[str, str]:
        """Return (authorization_url, state). Pass state to verify the callback."""
        self._code_verifier = secrets.token_urlsafe(64)
        digest = hashlib.sha256(self._code_verifier.encode()).digest()
        code_challenge = urlsafe_b64encode(digest).rstrip(b"=").decode()
        state = secrets.token_urlsafe(16)

        params = urlencode(
            {
                "response_type": "code",
                "redirect_uri": self.redirect_uri,
                "scope": " ".join(self._scopes),
                "client_id": self.api_key,
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
        )
        return f"{ETSY_AUTH_URL}?{params}", state

    def exchange_code(self, code: str) -> OAuthTokens:
        """Exchange an authorization code for tokens. Call get_auth_url() first."""
        if not self._code_verifier:
            raise ValueError("Call get_auth_url() before exchange_code()")

        response = httpx.post(
            ETSY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": self.api_key,
                "redirect_uri": self.redirect_uri,
                "code": code,
                "code_verifier": self._code_verifier,
            },
        )
        response.raise_for_status()
        data = response.json()

        tokens = OAuthTokens(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            # 60-second buffer so we refresh before the token actually expires
            expires_at=time.time() + data["expires_in"] - 60,
        )
        self._store.save(tokens)
        return tokens

    def refresh(self, tokens: OAuthTokens) -> OAuthTokens:
        """Obtain a new access token using the refresh token."""
        response = httpx.post(
            ETSY_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": self.api_key,
                "refresh_token": tokens.refresh_token,
            },
        )
        response.raise_for_status()
        data = response.json()

        new_tokens = OAuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", tokens.refresh_token),
            expires_at=time.time() + data["expires_in"] - 60,
        )
        self._store.save(new_tokens)
        return new_tokens

    def get_valid_tokens(self) -> OAuthTokens | None:
        """Return stored tokens, refreshing if expired. None if not yet authorized."""
        tokens = self._store.load()
        if tokens is None:
            return None
        if time.time() >= tokens.expires_at:
            tokens = self.refresh(tokens)
        return tokens
