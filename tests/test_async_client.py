"""Unit tests for the async client (AsyncSpeedAPI) with mocked httpx."""

from __future__ import annotations

import httpx
import pytest
import respx

from speedapi import AsyncSpeedAPI
from speedapi.models import CheckoutSessionStatus

BASE_URL = "https://api.tryspeed.com"

FAKE_SESSION = {
    "id": "cs_001",
    "status": "open",
    "amount": 5000,
    "currency": "USD",
    "url": "https://checkout.tryspeed.com/cs_001",
}

FAKE_BALANCE = {
    "available": [{"amount": 50000.0, "target_currency": "SATS"}],
    "pending": [],
}

FAKE_INVOICE = {
    "id": "inv_001",
    "status": "open",
    "amount": 10000,
    "currency": "USD",
}

FAKE_PR = {
    "id": "pr_001",
    "status": "pending",
    "amount": 21000,
    "currency": "SATS",
}


@pytest.fixture
def async_client(api_key):
    return AsyncSpeedAPI(api_key=api_key, base_url=BASE_URL)


class TestAsyncBalances:
    async def test_retrieve_balance(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.get("/balances").mock(
                return_value=httpx.Response(200, json=FAKE_BALANCE)
            )
            balance = await async_client.balances.retrieve()
            assert balance.available[0].amount == 50000.0
            assert balance.available[0].target_currency == "SATS"

    async def test_retrieve_sats(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.get("/balances").mock(
                return_value=httpx.Response(200, json=FAKE_BALANCE)
            )
            sats = await async_client.balances.retrieve_sats()
            assert sats == 50000.0


class TestAsyncCheckoutSessions:
    async def test_create_session(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.post("/checkout-sessions").mock(
                return_value=httpx.Response(200, json=FAKE_SESSION)
            )
            session = await async_client.checkout_sessions.create(
                amount=5000, currency="USD"
            )
            assert session.id == "cs_001"
            assert session.status == CheckoutSessionStatus.OPEN

    async def test_retrieve_session(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.get("/checkout-sessions/cs_001").mock(
                return_value=httpx.Response(200, json=FAKE_SESSION)
            )
            session = await async_client.checkout_sessions.retrieve("cs_001")
            assert session.url == "https://checkout.tryspeed.com/cs_001"


class TestAsyncInvoices:
    async def test_create_invoice(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.post("/invoices").mock(
                return_value=httpx.Response(200, json=FAKE_INVOICE)
            )
            invoice = await async_client.invoices.create(amount=10000, currency="USD")
            assert invoice.id == "inv_001"


class TestAsyncPayRequests:
    async def test_create_pay_request(self, async_client):
        with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
            router.post("/pay-requests").mock(
                return_value=httpx.Response(200, json=FAKE_PR)
            )
            pr = await async_client.pay_requests.create(amount=21000, currency="SATS")
            assert pr.id == "pr_001"
            assert pr.currency == "SATS"


class TestAsyncContextManager:
    async def test_context_manager_closes(self, api_key):
        async with AsyncSpeedAPI(api_key=api_key, base_url=BASE_URL) as client:
            with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
                router.get("/balances").mock(
                    return_value=httpx.Response(200, json=FAKE_BALANCE)
                )
                balance = await client.balances.retrieve()
                assert len(balance.available) == 1
