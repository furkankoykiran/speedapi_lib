"""Checkout Sessions resource — create, retrieve, list, expire."""

from __future__ import annotations

from typing import Any, Dict, Optional

from speedapi._http import SyncTransport
from speedapi.models import (
    CheckoutSession,
    CheckoutSessionList,
    CreateCheckoutSessionRequest,
    Currency,
)

_PATH = "/checkout-sessions"


class CheckoutSessions:
    """Checkout Sessions resource for the synchronous Speed API client.

    Access via :attr:`SpeedAPI.checkout_sessions`.

    Example:
        >>> session = client.checkout_sessions.create(amount=5000, currency="USD")
        >>> print(session.url)
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._http = transport

    def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CheckoutSession:
        """Create a new hosted checkout session.

        Args:
            amount: Amount to charge in the smallest currency unit (e.g. cents for USD).
            currency: ISO 4217 currency code or "SATS". Defaults to "USD".
            success_url: URL to redirect the customer to after a successful payment.
            cancel_url: URL to redirect the customer to if they click Cancel.
            description: Optional text shown on the checkout page.
            metadata: Optional key-value pairs to attach to the session.

        Returns:
            A :class:`~speedapi.models.CheckoutSession` object representing the new session.

        Raises:
            AuthenticationError: If the API key is invalid.
            APIStatusError: For other unexpected API errors.
        """
        req = CreateCheckoutSessionRequest(
            amount=amount,
            currency=Currency(currency),
            success_url=success_url,
            cancel_url=cancel_url,
            description=description,
            metadata=metadata,
        )
        data = self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return CheckoutSession.model_validate(data)

    def retrieve(self, session_id: str) -> CheckoutSession:
        """Retrieve an existing checkout session by ID.

        Args:
            session_id: The unique ID of the checkout session (e.g. ``cs_...``).

        Returns:
            The :class:`~speedapi.models.CheckoutSession` with the given ID.

        Raises:
            NotFoundError: If no session with the given ID exists.
        """
        data = self._http.get(f"{_PATH}/{session_id}")
        return CheckoutSession.model_validate(data)

    def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> CheckoutSessionList:
        """List checkout sessions, most recent first.

        Args:
            limit: Maximum number of sessions to return (1–100). Defaults to 20.
            starting_after: Cursor for forward pagination (session ID).
            ending_before: Cursor for backward pagination (session ID).

        Returns:
            A :class:`~speedapi.models.CheckoutSessionList` containing the results.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = self._http.get(_PATH, params=params)
        return CheckoutSessionList.model_validate(data)

    def expire(self, session_id: str) -> CheckoutSession:
        """Expire an open checkout session immediately.

        A session can only be expired if its status is ``open``.

        Args:
            session_id: The unique ID of the checkout session to expire.

        Returns:
            The updated :class:`~speedapi.models.CheckoutSession` with status ``expired``.

        Raises:
            NotFoundError: If no session with the given ID exists.
        """
        data = self._http.post(f"{_PATH}/{session_id}/expire")
        return CheckoutSession.model_validate(data)


class AsyncCheckoutSessions:
    """Checkout Sessions resource for the asynchronous Speed API client.

    Access via :attr:`AsyncSpeedAPI.checkout_sessions`.
    """

    def __init__(self, transport: Any) -> None:
        self._http = transport

    async def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CheckoutSession:
        """Create a new hosted checkout session (async).

        Args:
            amount: Amount in the smallest currency unit.
            currency: ISO 4217 currency code or "SATS". Defaults to "USD".
            success_url: Redirect URL on success.
            cancel_url: Redirect URL on cancel.
            description: Optional checkout page description.
            metadata: Optional key-value pairs.

        Returns:
            A :class:`~speedapi.models.CheckoutSession`.
        """
        req = CreateCheckoutSessionRequest(
            amount=amount,
            currency=Currency(currency),
            success_url=success_url,
            cancel_url=cancel_url,
            description=description,
            metadata=metadata,
        )
        data = await self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return CheckoutSession.model_validate(data)

    async def retrieve(self, session_id: str) -> CheckoutSession:
        """Retrieve a checkout session by ID (async).

        Args:
            session_id: The checkout session ID.

        Returns:
            A :class:`~speedapi.models.CheckoutSession`.
        """
        data = await self._http.get(f"{_PATH}/{session_id}")
        return CheckoutSession.model_validate(data)

    async def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> CheckoutSessionList:
        """List checkout sessions (async).

        Args:
            limit: Max sessions to return (1–100). Defaults to 20.
            starting_after: Forward pagination cursor.
            ending_before: Backward pagination cursor.

        Returns:
            A :class:`~speedapi.models.CheckoutSessionList`.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = await self._http.get(_PATH, params=params)
        return CheckoutSessionList.model_validate(data)

    async def expire(self, session_id: str) -> CheckoutSession:
        """Expire an open checkout session (async).

        Args:
            session_id: The checkout session ID.

        Returns:
            The updated :class:`~speedapi.models.CheckoutSession`.
        """
        data = await self._http.post(f"{_PATH}/{session_id}/expire")
        return CheckoutSession.model_validate(data)
