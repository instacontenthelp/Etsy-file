import pytest
import httpx

from etsy_file.api.client import EtsyClient
from etsy_file.api.exceptions import (
    AuthenticationError,
    EtsyAPIError,
    NotFoundError,
    RateLimitError,
)


def make_response(status_code: int, data: dict | None = None) -> httpx.Response:
    return httpx.Response(status_code, json=data or {})


@pytest.fixture
def client():
    return EtsyClient(api_key="test_key")


# ------------------------------------------------------------------
# Successful requests
# ------------------------------------------------------------------


def test_get_returns_json(client, mocker):
    mocker.patch.object(
        client._http, "request", return_value=make_response(200, {"listing_id": 99})
    )
    result = client.get("/application/shops/123/listings")
    assert result == {"listing_id": 99}


def test_post_returns_json(client, mocker):
    mocker.patch.object(
        client._http, "request", return_value=make_response(201, {"created": True})
    )
    result = client.post("/application/shops/123/listings", json={"title": "Test"})
    assert result == {"created": True}


# ------------------------------------------------------------------
# Rate limiting
# ------------------------------------------------------------------


def test_retries_on_429_then_succeeds(client, mocker):
    mocker.patch("etsy_file.api.client.time.sleep")
    mocker.patch.object(
        client._http,
        "request",
        side_effect=[make_response(429), make_response(200, {"ok": True})],
    )
    result = client.get("/some/path")
    assert result == {"ok": True}


def test_raises_rate_limit_after_max_retries(client, mocker):
    mocker.patch("etsy_file.api.client.time.sleep")
    mocker.patch.object(
        client._http, "request", return_value=make_response(429)
    )
    with pytest.raises(RateLimitError):
        client.get("/some/path")


def test_retry_delay_doubles(client, mocker):
    mock_sleep = mocker.patch("etsy_file.api.client.time.sleep")
    mocker.patch.object(
        client._http,
        "request",
        side_effect=[
            make_response(429),
            make_response(429),
            make_response(200, {}),
        ],
    )
    client.get("/some/path")
    assert mock_sleep.call_args_list[0].args[0] == 1.0
    assert mock_sleep.call_args_list[1].args[0] == 2.0


# ------------------------------------------------------------------
# Error responses
# ------------------------------------------------------------------


def test_raises_authentication_error_on_401(client, mocker):
    mocker.patch.object(
        client._http, "request", return_value=make_response(401)
    )
    with pytest.raises(AuthenticationError) as exc_info:
        client.get("/protected")
    assert exc_info.value.status_code == 401


def test_raises_not_found_on_404(client, mocker):
    mocker.patch.object(
        client._http, "request", return_value=make_response(404)
    )
    with pytest.raises(NotFoundError) as exc_info:
        client.get("/missing")
    assert exc_info.value.status_code == 404


def test_raises_etsy_api_error_on_500(client, mocker):
    mocker.patch.object(
        client._http, "request", return_value=make_response(500)
    )
    with pytest.raises(EtsyAPIError) as exc_info:
        client.get("/boom")
    assert exc_info.value.status_code == 500


# ------------------------------------------------------------------
# Auth header injection
# ------------------------------------------------------------------


def test_no_auth_header_without_auth_object(client, mocker):
    mock_request = mocker.patch.object(
        client._http, "request", return_value=make_response(200, {})
    )
    client.get("/path")
    _, kwargs = mock_request.call_args
    assert "Authorization" not in kwargs.get("headers", {})


def test_bearer_token_injected_when_auth_present(mocker):
    from etsy_file.api.auth import EtsyAuth, OAuthTokens
    import time

    mock_auth = mocker.MagicMock(spec=EtsyAuth)
    mock_auth.get_valid_tokens.return_value = OAuthTokens(
        access_token="live_token",
        refresh_token="r",
        expires_at=time.time() + 3600,
    )

    c = EtsyClient(api_key="key", auth=mock_auth)
    mock_request = mocker.patch.object(
        c._http, "request", return_value=make_response(200, {})
    )
    c.get("/path")

    _, kwargs = mock_request.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer live_token"


# ------------------------------------------------------------------
# Context manager
# ------------------------------------------------------------------


def test_context_manager_closes_client(mocker):
    mock_close = mocker.patch.object(EtsyClient, "close")
    with EtsyClient(api_key="key"):
        pass
    mock_close.assert_called_once()
