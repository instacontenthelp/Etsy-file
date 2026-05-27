import time

import pytest

from etsy_file.api.auth import EtsyAuth, OAuthTokens, TokenStore


@pytest.fixture
def token_file(tmp_path):
    return str(tmp_path / "tokens.json")


@pytest.fixture
def auth(token_file):
    return EtsyAuth(
        api_key="test_key",
        api_secret="test_secret",
        redirect_uri="http://localhost:8000/oauth/callback",
        token_file=token_file,
    )


# ------------------------------------------------------------------
# TokenStore
# ------------------------------------------------------------------


def test_token_store_save_and_load(token_file):
    store = TokenStore(token_file)
    tokens = OAuthTokens(
        access_token="abc123",
        refresh_token="xyz789",
        expires_at=time.time() + 3600,
    )
    store.save(tokens)
    loaded = store.load()
    assert loaded.access_token == "abc123"
    assert loaded.refresh_token == "xyz789"


def test_token_store_load_returns_none_when_missing(token_file):
    store = TokenStore(token_file)
    assert store.load() is None


# ------------------------------------------------------------------
# EtsyAuth.get_auth_url
# ------------------------------------------------------------------


def test_get_auth_url_contains_required_params(auth):
    url, state = auth.get_auth_url()
    assert "etsy.com/oauth/connect" in url
    assert "code_challenge" in url
    assert "code_challenge_method=S256" in url
    assert f"client_id=test_key" in url
    assert len(state) > 8


def test_get_auth_url_sets_code_verifier(auth):
    assert auth._code_verifier is None
    auth.get_auth_url()
    assert auth._code_verifier is not None


# ------------------------------------------------------------------
# EtsyAuth.exchange_code
# ------------------------------------------------------------------


def test_exchange_code_raises_without_verifier(auth):
    with pytest.raises(ValueError, match="get_auth_url"):
        auth.exchange_code("some_code")


def test_exchange_code_stores_and_returns_tokens(auth, mocker):
    auth.get_auth_url()

    mock_post = mocker.patch("etsy_file.api.auth.httpx.post")
    mock_post.return_value.json.return_value = {
        "access_token": "new_access",
        "refresh_token": "new_refresh",
        "expires_in": 3600,
    }
    mock_post.return_value.raise_for_status = lambda: None

    tokens = auth.exchange_code("auth_code_abc")

    assert tokens.access_token == "new_access"
    assert tokens.refresh_token == "new_refresh"
    assert tokens.expires_at > time.time()

    stored = auth._store.load()
    assert stored.access_token == "new_access"


# ------------------------------------------------------------------
# EtsyAuth.get_valid_tokens
# ------------------------------------------------------------------


def test_get_valid_tokens_returns_none_when_no_file(auth):
    assert auth.get_valid_tokens() is None


def test_get_valid_tokens_returns_fresh_tokens(auth):
    fresh = OAuthTokens("access", "refresh", time.time() + 3600)
    auth._store.save(fresh)
    result = auth.get_valid_tokens()
    assert result.access_token == "access"


def test_get_valid_tokens_refreshes_expired(auth, mocker):
    expired = OAuthTokens("old_access", "old_refresh", time.time() - 1)
    auth._store.save(expired)

    refreshed = OAuthTokens("new_access", "new_refresh", time.time() + 3600)
    mock_refresh = mocker.patch.object(auth, "refresh", return_value=refreshed)

    result = auth.get_valid_tokens()

    mock_refresh.assert_called_once()
    assert result.access_token == "new_access"
