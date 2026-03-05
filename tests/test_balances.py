"""Balances resource tests."""
from __future__ import annotations

import httpx
import pytest

from speedapi import SpeedAPI

BASE_URL = "https://api.tryspeed.com"

FAKE_BALANCE = {
    "available": [
        {"amount": 50000.0, "target_currency": "SATS"},
        {"amount": 100.0, "target_currency": "USD"},
    ],
    "pending": [{"amount": 1000.0, "target_currency": "SATS"}],
}


@pytest.fixture
def client(api_key):
    return SpeedAPI(api_key=api_key, base_url=BASE_URL)


class TestBalancesRetrieve:
    def test_retrieves_balance(self, client, mock_router):
        mock_router.get("/balances").mock(
            return_value=httpx.Response(200, json=FAKE_BALANCE)
        )
        balance = client.balances.retrieve()
        assert len(balance.available) == 2
        assert balance.available[0].target_currency == "SATS"
        assert balance.pending[0].amount == 1000.0

    def test_retrieve_sats(self, client, mock_router):
        mock_router.get("/balances").mock(
            return_value=httpx.Response(200, json=FAKE_BALANCE)
        )
        sats = client.balances.retrieve_sats()
        assert sats == 50000.0

    def test_retrieve_sats_returns_zero_when_absent(self, client, mock_router):
        mock_router.get("/balances").mock(
            return_value=httpx.Response(200, json={"available": [], "pending": []})
        )
        sats = client.balances.retrieve_sats()
        assert sats == 0.0

    def test_context_manager_closes(self, api_key, mock_router):
        mock_router.get("/balances").mock(
            return_value=httpx.Response(200, json=FAKE_BALANCE)
        )
        with SpeedAPI(api_key=api_key, base_url=BASE_URL) as client:
            balance = client.balances.retrieve()
            assert len(balance.available) == 2
