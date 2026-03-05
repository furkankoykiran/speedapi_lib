"""Unit tests for Pydantic v2 models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from speedapi.models import (
    Balance,
    CheckoutSession,
    CheckoutSessionStatus,
    Currency,
    Invoice,
    InvoiceStatus,
    PayRequest,
    PayRequestStatus,
    WebhookEvent,
)


class TestCurrency:
    def test_valid_currencies(self):
        for c in ("USD", "EUR", "GBP", "SATS", "BTC"):
            assert Currency(c).value == c

    def test_invalid_currency_raises(self):
        with pytest.raises(ValueError):
            Currency("XYZ")


class TestBalanceModel:
    def test_parses_correctly(self):
        data = {
            "available": [{"amount": 21000.0, "target_currency": "SATS"}],
            "pending": [],
        }
        balance = Balance.model_validate(data)
        assert len(balance.available) == 1
        assert balance.available[0].amount == 21000.0
        assert balance.available[0].target_currency == "SATS"

    def test_defaults_to_empty_lists(self):
        balance = Balance.model_validate({})
        assert balance.available == []
        assert balance.pending == []


class TestCheckoutSessionModel:
    def test_minimal_valid(self):
        session = CheckoutSession.model_validate(
            {"id": "cs_001", "amount": 5000, "currency": "USD"}
        )
        assert session.id == "cs_001"
        assert session.status == CheckoutSessionStatus.OPEN

    def test_extra_fields_allowed(self):
        session = CheckoutSession.model_validate(
            {"id": "cs_001", "amount": 5000, "currency": "USD", "future_field": "x"}
        )
        assert session.id == "cs_001"

    def test_id_required(self):
        with pytest.raises(ValidationError):
            CheckoutSession.model_validate({"amount": 5000, "currency": "USD"})


class TestInvoiceModel:
    def test_minimal_valid(self):
        inv = Invoice.model_validate(
            {"id": "inv_001", "amount": 10000, "currency": "USD"}
        )
        assert inv.id == "inv_001"
        assert inv.status == InvoiceStatus.OPEN

    def test_optional_fields_none(self):
        inv = Invoice.model_validate(
            {"id": "inv_001", "amount": 10000, "currency": "USD"}
        )
        assert inv.customer_email is None
        assert inv.hosted_invoice_url is None


class TestPayRequestModel:
    def test_minimal_valid(self):
        pr = PayRequest.model_validate(
            {"id": "pr_001", "amount": 1000, "currency": "SATS"}
        )
        assert pr.id == "pr_001"
        assert pr.status == PayRequestStatus.PENDING

    def test_lightning_invoice_optional(self):
        pr = PayRequest.model_validate(
            {"id": "pr_001", "amount": 1000, "currency": "SATS"}
        )
        assert pr.lightning_invoice is None


class TestWebhookEventModel:
    def test_parses_event(self):
        event = WebhookEvent.model_validate(
            {
                "id": "evt_001",
                "type": "checkout_session.completed",
                "created": 1700000000,
                "data": {"object": {"id": "cs_001"}},
                "livemode": True,
            }
        )
        assert event.id == "evt_001"
        assert event.type == "checkout_session.completed"
        assert event.data["object"]["id"] == "cs_001"
