"""Unit tests for the exception hierarchy and HTTP → exception mapping."""

from __future__ import annotations

import httpx
import pytest

from speedapi import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SpeedAPIError,
)
from speedapi._http import SyncTransport, _raise_for_status

BASE_URL = "https://api.tryspeed.com"


def _make_response(status_code: int, text: str = "") -> httpx.Response:
    return httpx.Response(status_code, text=text)


class TestExceptionHierarchy:
    def test_all_errors_are_speed_api_errors(self):
        for cls in (
            AuthenticationError,
            PermissionDeniedError,
            NotFoundError,
            RateLimitError,
            APIStatusError,
            APIConnectionError,
        ):
            assert issubclass(cls, SpeedAPIError)

    def test_base_error_stores_message_and_status(self):
        err = APIStatusError("boom", status_code=500, response_body="error body")
        assert err.message == "boom"
        assert err.status_code == 500
        assert err.response_body == "error body"

    def test_connection_error_has_no_status(self):
        err = APIConnectionError("DNS failure")
        assert err.status_code is None


class TestRaiseForStatus:
    def test_success_does_not_raise(self):
        _raise_for_status(_make_response(200))
        _raise_for_status(_make_response(201))

    def test_401_raises_authentication_error(self):
        with pytest.raises(AuthenticationError):
            _raise_for_status(_make_response(401))

    def test_403_raises_permission_denied(self):
        with pytest.raises(PermissionDeniedError):
            _raise_for_status(_make_response(403))

    def test_404_raises_not_found(self):
        with pytest.raises(NotFoundError):
            _raise_for_status(_make_response(404))

    def test_429_raises_rate_limit(self):
        with pytest.raises(RateLimitError):
            _raise_for_status(_make_response(429))

    def test_500_raises_api_status_error(self):
        with pytest.raises(APIStatusError) as exc_info:
            _raise_for_status(_make_response(500, "internal error"))
        assert exc_info.value.status_code == 500


class TestAPIConnectionError:
    def test_network_error_is_wrapped(self, api_key):
        """Verify that httpx.ConnectError is wrapped into APIConnectionError."""

        class _FailingTransport(httpx.BaseTransport):
            def handle_request(self, request):
                raise httpx.ConnectError("DNS failure")

        transport = SyncTransport(api_key=api_key, base_url=BASE_URL)
        transport._client = httpx.Client(
            base_url=BASE_URL,
            transport=_FailingTransport(),
        )
        with pytest.raises(APIConnectionError, match="Network error"):
            transport.get("/balances")
