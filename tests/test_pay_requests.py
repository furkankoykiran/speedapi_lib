"""Unit tests for the Pay Requests resource (mocked)."""

from __future__ import annotations

import httpx
import pytest

from speedapi import SpeedAPI
from speedapi.models import PayRequestStatus

BASE_URL = "https://api.tryspeed.com"

FAKE_PR = {
    "id": "pr_001",
    "status": "pending",
    "amount": 21000,
    "currency": "SATS",
    "description": "Coffee payment",
    "payment_url": "https://pay.tryspeed.com/pr_001",
    "lightning_invoice": "lnbc210u1p...",
}


@pytest.fixture
def client(api_key):
    return SpeedAPI(api_key=api_key, base_url=BASE_URL)


class TestPayRequestsCreate:
    def test_creates_pay_request(self, client, mock_router):
        mock_router.post("/pay-requests").mock(return_value=httpx.Response(200, json=FAKE_PR))
        pr = client.pay_requests.create(amount=21000, currency="SATS", description="Coffee payment")
        assert pr.id == "pr_001"
        assert pr.status == PayRequestStatus.PENDING
        assert pr.lightning_invoice == "lnbc210u1p..."


class TestPayRequestsRetrieve:
    def test_retrieves_by_id(self, client, mock_router):
        mock_router.get("/pay-requests/pr_001").mock(return_value=httpx.Response(200, json=FAKE_PR))
        pr = client.pay_requests.retrieve("pr_001")
        assert pr.id == "pr_001"

    def test_not_found_raises(self, client, mock_router):
        from speedapi import NotFoundError

        mock_router.get("/pay-requests/bad").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(NotFoundError):
            client.pay_requests.retrieve("bad")


class TestPayRequestsList:
    def test_lists_pay_requests(self, client, mock_router):
        payload = {"data": [FAKE_PR], "has_more": False}
        mock_router.get("/pay-requests").mock(return_value=httpx.Response(200, json=payload))
        result = client.pay_requests.list()
        assert len(result.data) == 1
        assert result.data[0].currency == "SATS"
