"""Synchronous Speed API client."""

from __future__ import annotations

from speedapi._http import SyncTransport
from speedapi.models import Balance
from speedapi.resources.checkout_sessions import CheckoutSessions
from speedapi.resources.invoices import Invoices
from speedapi.resources.pay_requests import PayRequests


class SpeedAPI:
    """Synchronous Python client for the Speed Merchant API.

    Provides access to all Speed API resources through a simple, attribute-style
    interface. Each resource (e.g. ``checkout_sessions``) is an instance of the
    corresponding resource class.

    Args:
        api_key: Your Speed secret API key (``sk_live_...`` or ``sk_test_...``).
        base_url: Override the default Speed API base URL. Useful for testing.
        timeout: Default request timeout in seconds. Defaults to 30.

    Example:
        >>> from speedapi import SpeedAPI
        >>> client = SpeedAPI(api_key="sk_live_...")
        >>> balance = client.balances.retrieve()
        >>> print(f"Available: {balance.available}")
        >>>
        >>> session = client.checkout_sessions.create(
        ...     amount=5000,
        ...     currency="USD",
        ...     success_url="https://example.com/success",
        ... )
        >>> print(session.url)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tryspeed.com",
        timeout: float = 30.0,
    ) -> None:
        self._transport = SyncTransport(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.checkout_sessions = CheckoutSessions(self._transport)
        self.invoices = Invoices(self._transport)
        self.pay_requests = PayRequests(self._transport)
        self.balances = _BalancesResource(self._transport)

    def close(self) -> None:
        """Close the underlying HTTP connection pool.

        Call this when you're done using the client outside of a context manager.
        """
        self._transport.close()

    def __enter__(self) -> SpeedAPI:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class _BalancesResource:
    """Balances resource — retrieve the merchant's current balance."""

    def __init__(self, transport: SyncTransport) -> None:
        self._http = transport

    def retrieve(self) -> Balance:
        """Retrieve the merchant's current balance across all currencies.

        Returns:
            A :class:`~speedapi.models.Balance` containing available and pending
            items for each currency.

        Raises:
            AuthenticationError: If the API key is invalid.

        Example:
            >>> balance = client.balances.retrieve()
            >>> sats = next(
            ...     (b.amount for b in balance.available if b.target_currency == "SATS"),
            ...     0,
            ... )
            >>> print(f"Available SATS: {sats}")
        """
        data = self._http.get("/balances")
        return Balance.model_validate(data)

    def retrieve_sats(self) -> float:
        """Retrieve the available balance in SATS (satoshis).

        A convenience wrapper around :meth:`retrieve` that extracts the SATS
        balance directly.

        Returns:
            Available balance in SATS. Returns ``0.0`` if no SATS balance exists.

        Example:
            >>> sats = client.balances.retrieve_sats()
            >>> print(f"Available: {sats} SATS")
        """
        balance = self.retrieve()
        for item in balance.available:
            if item.target_currency == "SATS":
                return float(item.amount)
        return 0.0
