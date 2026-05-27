"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def etsy_api_key() -> str:
    return "test_api_key"


@pytest.fixture
def etsy_shop_id() -> str:
    return "12345678"
