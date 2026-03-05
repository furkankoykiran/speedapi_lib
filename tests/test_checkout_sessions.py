"""Unit tests for the CheckoutSessions resource (mocked)."""

from __future__ import annotations

import json

import httpx
import pytest

from speedapi import SpeedAPI
from speedapi.models import CheckoutSessionStatus

BASE_URL = "https://api.tryspeed.com"

FAKE_SESSION = {
    "id": "cs_001",
    "status": "open",
    "amount": 5000,
    "currency": "USD",
    "url": "https://checkout.tryspeed.com/cs_001",
    "success_url": "https://example.com/success",
    "cancel_url": "https://example.com/cancel",
}


@pytest.fixture
def client(api_key):
    return SpeedAPI(api_key=api_key, base_url=BASE_URL)


class TestCheckoutSessionsCreate:
    def test_creates_session(self, client, mock_router):
        mock_router.post("/checkout-sessions").mock(
            return_value=httpx.Response(200, json=FAKE_SESSION)
        )
        session = client.checkout_sessions.create(
            amount=5000,
            currency="USD",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        assert session.id == "cs_001"
        assert session.status == CheckoutSessionStatus.OPEN
        assert session.url == "https://checkout.tryspeed.com/cs_001"

    def test_sends_correct_payload(self, client, mock_router):
        captured = {}

        def capture(request, route):
            captured["body"] = json.loads(request.content)
            return httpx.Response(200, json=FAKE_SESSION)

        mock_router.post("/checkout-sessions").mock(side_effect=capture)
        client.checkout_sessions.create(amount=5000, currency="USD")
        assert captured["body"]["amount"] == 5000
        assert captured["body"]["currency"] == "USD"


class TestCheckoutSessionsRetrieve:
    def test_retrieves_by_id(self, client, mock_router):
        mock_router.get("/checkout-sessions/cs_001").mock(
            return_value=httpx.Response(200, json=FAKE_SESSION)
        )
        session = client.checkout_sessions.retrieve("cs_001")
        assert session.id == "cs_001"

    def test_not_found_raises(self, client, mock_router):
        from speedapi import NotFoundError
        mock_router.get("/checkout-sessions/bad_id").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(NotFoundError):
            client.checkout_sessions.retrieve("bad_id")


class TestCheckoutSessionsList:
    def test_lists_sessions(self, client, mock_router):
        payload = {"data": [FAKE_SESSION], "has_more": False}
        mock_router.get("/checkout-sessions").mock(
            return_value=httpx.Response(200, json=payload)
        )
        result = client.checkout_sessions.list(limit=10)
        assert len(result.data) == 1
        assert result.has_more is False


class TestCheckoutSessionsExpire:
    def test_expires_session(self, client, mock_router):
        expired = {**FAKE_SESSION, "status": "expired"}
        mock_router.post("/checkout-sessions/cs_001/expire").mock(
            return_value=httpx.Response(200, json=expired)
        )
        session = client.checkout_sessions.expire("cs_001")
        assert session.status == CheckoutSessionStatus.EXPIRED
