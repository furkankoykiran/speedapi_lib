"""Unit tests for the Invoices resource (mocked)."""

from __future__ import annotations

import httpx
import pytest

from speedapi import SpeedAPI
from speedapi.models import InvoiceStatus

BASE_URL = "https://api.tryspeed.com"

FAKE_INVOICE = {
    "id": "inv_001",
    "status": "open",
    "amount": 10000,
    "currency": "USD",
    "description": "Order #42",
    "customer_email": "customer@example.com",
    "hosted_invoice_url": "https://invoice.tryspeed.com/inv_001",
}


@pytest.fixture
def client(api_key):
    return SpeedAPI(api_key=api_key, base_url=BASE_URL)


class TestInvoicesCreate:
    def test_creates_invoice(self, client, mock_router):
        mock_router.post("/invoices").mock(
            return_value=httpx.Response(200, json=FAKE_INVOICE)
        )
        invoice = client.invoices.create(
            amount=10000,
            currency="USD",
            description="Order #42",
            customer_email="customer@example.com",
        )
        assert invoice.id == "inv_001"
        assert invoice.status == InvoiceStatus.OPEN
        assert invoice.hosted_invoice_url == "https://invoice.tryspeed.com/inv_001"


class TestInvoicesRetrieve:
    def test_retrieves_by_id(self, client, mock_router):
        mock_router.get("/invoices/inv_001").mock(
            return_value=httpx.Response(200, json=FAKE_INVOICE)
        )
        invoice = client.invoices.retrieve("inv_001")
        assert invoice.id == "inv_001"

    def test_not_found_raises(self, client, mock_router):
        from speedapi import NotFoundError
        mock_router.get("/invoices/bad").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(NotFoundError):
            client.invoices.retrieve("bad")


class TestInvoicesList:
    def test_lists_invoices(self, client, mock_router):
        payload = {"data": [FAKE_INVOICE], "has_more": True}
        mock_router.get("/invoices").mock(
            return_value=httpx.Response(200, json=payload)
        )
        result = client.invoices.list()
        assert len(result.data) == 1
        assert result.has_more is True
