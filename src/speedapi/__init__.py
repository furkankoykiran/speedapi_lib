"""
speedapi — Python SDK for the Speed Merchant API.

Usage (sync):
    from speedapi import SpeedAPI
    client = SpeedAPI(api_key="sk_live_...")
    balance = client.balances.retrieve()

Usage (async):
    from speedapi import AsyncSpeedAPI
    async with AsyncSpeedAPI(api_key="sk_live_...") as client:
        session = await client.checkout_sessions.create(amount=5000, currency="USD")
"""

from speedapi import models
from speedapi.async_client import AsyncSpeedAPI
from speedapi.client import SpeedAPI
from speedapi.exceptions import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SpeedAPIError,
)

__all__ = [
    "SpeedAPI",
    "AsyncSpeedAPI",
    "SpeedAPIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "RateLimitError",
    "APIStatusError",
    "APIConnectionError",
    "models",
]

__version__ = "2.0.2"
