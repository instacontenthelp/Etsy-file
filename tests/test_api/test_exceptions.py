from etsy_file.api.exceptions import (
    AuthenticationError,
    EtsyAPIError,
    NotFoundError,
    RateLimitError,
)


def test_etsy_api_error_message():
    err = EtsyAPIError(500, "server error")
    assert err.status_code == 500
    assert "500" in str(err)
    assert "server error" in str(err)


def test_subclasses_are_etsy_api_errors():
    assert issubclass(RateLimitError, EtsyAPIError)
    assert issubclass(AuthenticationError, EtsyAPIError)
    assert issubclass(NotFoundError, EtsyAPIError)
