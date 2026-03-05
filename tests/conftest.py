"""Shared pytest fixtures for the Speed API SDK test suite."""

from __future__ import annotations

import pytest
import respx

FAKE_API_KEY = "sk_test_fake_key_for_testing_only"
BASE_URL = "https://api.tryspeed.com"


@pytest.fixture
def api_key() -> str:
    """Return a fake API key for tests."""
    return FAKE_API_KEY


@pytest.fixture
def mock_router():
    """Activate a respx mock router for the Speed API base URL.

    Yields:
        An active :class:`respx.MockRouter` instance. Any request to
        ``https://api.tryspeed.com`` that is not mocked will raise an error.
    """
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
        yield router
