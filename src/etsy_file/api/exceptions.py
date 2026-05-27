class EtsyAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class RateLimitError(EtsyAPIError):
    pass


class AuthenticationError(EtsyAPIError):
    pass


class NotFoundError(EtsyAPIError):
    pass
