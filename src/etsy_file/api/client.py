import time
from typing import Any

import httpx

from .auth import EtsyAuth
from .exceptions import AuthenticationError, EtsyAPIError, NotFoundError, RateLimitError

BASE_URL = "https://openapi.etsy.com/v3"
_MAX_RETRIES = 3


class EtsyClient:
    def __init__(self, api_key: str, auth: EtsyAuth | None = None) -> None:
        self.api_key = api_key
        self.auth = auth
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={"x-api-key": api_key},
            timeout=30.0,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _auth_headers(self) -> dict[str, str]:
        if self.auth is None:
            return {}
        tokens = self.auth.get_valid_tokens()
        if tokens is None:
            return {}
        return {"Authorization": f"Bearer {tokens.access_token}"}

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers = self._auth_headers()
        delay = 1.0

        for attempt in range(_MAX_RETRIES):
            response = self._http.request(method, path, headers=headers, **kwargs)

            if response.status_code == 429:
                if attempt == _MAX_RETRIES - 1:
                    raise RateLimitError(429, "Rate limit exceeded after retries")
                time.sleep(delay)
                delay *= 2
                continue

            if response.status_code == 401:
                raise AuthenticationError(401, response.text)

            if response.status_code == 404:
                raise NotFoundError(404, response.text)

            if not response.is_success:
                raise EtsyAPIError(response.status_code, response.text)

            return response.json()

        raise RateLimitError(429, "Rate limit exceeded after retries")

    # ------------------------------------------------------------------
    # Public HTTP methods
    # ------------------------------------------------------------------

    def get(self, path: str, **kwargs: Any) -> Any:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self._request("DELETE", path, **kwargs)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "EtsyClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
