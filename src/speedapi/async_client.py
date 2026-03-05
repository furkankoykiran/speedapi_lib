"""Asynchronous Speed API client."""

from __future__ import annotations

from speedapi._http import AsyncTransport
from speedapi.models import Balance
from speedapi.resources.checkout_sessions import AsyncCheckoutSessions
from speedapi.resources.invoices import AsyncInvoices
from speedapi.resources.pay_requests import AsyncPayRequests


class AsyncSpeedAPI:
    """Asynchronous Python client for the Speed Merchant API.

    Designed for use in async contexts (e.g. FastAPI, aiohttp) with ``async/await``.
    Best used as an asynchronous context manager to ensure the connection pool
    is properly closed.

    Args:
        api_key: Your Speed secret API key (``sk_live_...`` or ``sk_test_...``).
        base_url: Override the default Speed API base URL.
        timeout: Default request timeout in seconds. Defaults to 30.

    Example:
        >>> import asyncio
        >>> from speedapi import AsyncSpeedAPI
        >>>
        >>> async def main():
        ...     async with AsyncSpeedAPI(api_key="sk_live_...") as client:
        ...         balance = await client.balances.retrieve()
        ...         session = await client.checkout_sessions.create(
        ...             amount=5000,
        ...             currency="USD",
        ...             success_url="https://example.com/success",
        ...         )
        ...         print(session.url)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tryspeed.com",
        timeout: float = 30.0,
    ) -> None:
        self._transport = AsyncTransport(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.checkout_sessions = AsyncCheckoutSessions(self._transport)
        self.invoices = AsyncInvoices(self._transport)
        self.pay_requests = AsyncPayRequests(self._transport)
        self.balances = _AsyncBalancesResource(self._transport)

    async def aclose(self) -> None:
        """Close the underlying async HTTP connection pool."""
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncSpeedAPI:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()


class _AsyncBalancesResource:
    """Async Balances resource."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._http = transport

    async def retrieve(self) -> Balance:
        """Retrieve the merchant's current balance (async).

        Returns:
            A :class:`~speedapi.models.Balance` containing available and pending
            items for each currency.

        Raises:
            AuthenticationError: If the API key is invalid.
        """
        data = await self._http.get("/balances")
        return Balance.model_validate(data)

    async def retrieve_sats(self) -> float:
        """Retrieve the available SATS balance (async).

        Returns:
            Available balance in SATS.  Returns ``0.0`` if no SATS balance exists.
        """
        balance = await self.retrieve()
        for item in balance.available:
            if item.target_currency == "SATS":
                return float(item.amount)
        return 0.0
