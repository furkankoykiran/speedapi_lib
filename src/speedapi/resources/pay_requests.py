"""Pay Requests resource — create, retrieve, list."""

from __future__ import annotations

from typing import Any, Dict, Optional

from speedapi._http import SyncTransport
from speedapi.models import (
    CreatePayRequestRequest,
    Currency,
    PayRequest,
    PayRequestList,
)

_PATH = "/pay-requests"


class PayRequests:
    """Pay Requests resource for the synchronous Speed API client.

    Access via :attr:`SpeedAPI.pay_requests`.

    Example:
        >>> pr = client.pay_requests.create(amount=21000, currency="SATS")
        >>> print(pr.lightning_invoice)
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._http = transport

    def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        description: Optional[str] = None,
        expires_in: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PayRequest:
        """Create a new pay request.

        Args:
            amount: Amount in the smallest currency unit.
            currency: ISO 4217 code or "SATS". Defaults to "USD".
            description: Human-readable description.
            expires_in: Seconds until the pay request expires.
            metadata: Optional key-value pairs.

        Returns:
            A :class:`~speedapi.models.PayRequest` object.
        """
        req = CreatePayRequestRequest(
            amount=amount,
            currency=Currency(currency),
            description=description,
            expires_in=expires_in,
            metadata=metadata,
        )
        data = self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return PayRequest.model_validate(data)

    def retrieve(self, pay_request_id: str) -> PayRequest:
        """Retrieve a pay request by ID.

        Args:
            pay_request_id: The pay request ID (e.g. ``pr_...``).

        Returns:
            A :class:`~speedapi.models.PayRequest`.

        Raises:
            NotFoundError: If no pay request with the given ID exists.
        """
        data = self._http.get(f"{_PATH}/{pay_request_id}")
        return PayRequest.model_validate(data)

    def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> PayRequestList:
        """List pay requests, most recent first.

        Args:
            limit: Max pay requests to return (1–100). Defaults to 20.
            starting_after: Forward pagination cursor.
            ending_before: Backward pagination cursor.

        Returns:
            A :class:`~speedapi.models.PayRequestList`.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = self._http.get(_PATH, params=params)
        return PayRequestList.model_validate(data)


class AsyncPayRequests:
    """Pay Requests resource for the asynchronous Speed API client."""

    def __init__(self, transport: Any) -> None:
        self._http = transport

    async def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        description: Optional[str] = None,
        expires_in: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PayRequest:
        """Create a new pay request (async).

        Args:
            amount: Amount in the smallest currency unit.
            currency: ISO 4217 code or "SATS". Defaults to "USD".
            description: Human-readable description.
            expires_in: Seconds until expiry.
            metadata: Optional key-value pairs.

        Returns:
            A :class:`~speedapi.models.PayRequest`.
        """
        req = CreatePayRequestRequest(
            amount=amount,
            currency=Currency(currency),
            description=description,
            expires_in=expires_in,
            metadata=metadata,
        )
        data = await self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return PayRequest.model_validate(data)

    async def retrieve(self, pay_request_id: str) -> PayRequest:
        """Retrieve a pay request by ID (async).

        Args:
            pay_request_id: The pay request ID.

        Returns:
            A :class:`~speedapi.models.PayRequest`.
        """
        data = await self._http.get(f"{_PATH}/{pay_request_id}")
        return PayRequest.model_validate(data)

    async def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> PayRequestList:
        """List pay requests (async).

        Args:
            limit: Max pay requests to return. Defaults to 20.
            starting_after: Forward pagination cursor.
            ending_before: Backward pagination cursor.

        Returns:
            A :class:`~speedapi.models.PayRequestList`.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = await self._http.get(_PATH, params=params)
        return PayRequestList.model_validate(data)
