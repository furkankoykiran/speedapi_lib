"""Invoices resource — create, retrieve, list."""

from __future__ import annotations

from typing import Any, Dict, Optional

from speedapi._http import SyncTransport
from speedapi.models import (
    CreateInvoiceRequest,
    Currency,
    Invoice,
    InvoiceList,
)

_PATH = "/invoices"


class Invoices:
    """Invoices resource for the synchronous Speed API client.

    Access via :attr:`SpeedAPI.invoices`.

    Example:
        >>> invoice = client.invoices.create(amount=10000, currency="USD", description="Order #42")
        >>> print(invoice.hosted_invoice_url)
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._http = transport

    def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        description: Optional[str] = None,
        customer_email: Optional[str] = None,
        due_date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Invoice:
        """Create a new invoice.

        Args:
            amount: Amount in the smallest currency unit.
            currency: ISO 4217 code or "SATS". Defaults to "USD".
            description: Human-readable invoice description.
            customer_email: Email address to send the invoice to.
            due_date: ISO 8601 due date (e.g. ``"2025-12-31"``).
            metadata: Optional key-value pairs.

        Returns:
            A :class:`~speedapi.models.Invoice` object.
        """
        req = CreateInvoiceRequest(
            amount=amount,
            currency=Currency(currency),
            description=description,
            customer_email=customer_email,
            due_date=due_date,
            metadata=metadata,
        )
        data = self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return Invoice.model_validate(data)

    def retrieve(self, invoice_id: str) -> Invoice:
        """Retrieve an invoice by ID.

        Args:
            invoice_id: The invoice ID (e.g. ``inv_...``).

        Returns:
            A :class:`~speedapi.models.Invoice`.

        Raises:
            NotFoundError: If no invoice with the given ID exists.
        """
        data = self._http.get(f"{_PATH}/{invoice_id}")
        return Invoice.model_validate(data)

    def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> InvoiceList:
        """List invoices, most recent first.

        Args:
            limit: Max invoices to return (1–100). Defaults to 20.
            starting_after: Forward pagination cursor.
            ending_before: Backward pagination cursor.

        Returns:
            A :class:`~speedapi.models.InvoiceList`.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = self._http.get(_PATH, params=params)
        return InvoiceList.model_validate(data)


class AsyncInvoices:
    """Invoices resource for the asynchronous Speed API client."""

    def __init__(self, transport: Any) -> None:
        self._http = transport

    async def create(
        self,
        amount: int,
        currency: str = "USD",
        *,
        description: Optional[str] = None,
        customer_email: Optional[str] = None,
        due_date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Invoice:
        """Create a new invoice (async).

        Args:
            amount: Amount in the smallest currency unit.
            currency: ISO 4217 code or "SATS". Defaults to "USD".
            description: Invoice description.
            customer_email: Customer email.
            due_date: ISO 8601 due date.
            metadata: Optional key-value pairs.

        Returns:
            A :class:`~speedapi.models.Invoice`.
        """
        req = CreateInvoiceRequest(
            amount=amount,
            currency=Currency(currency),
            description=description,
            customer_email=customer_email,
            due_date=due_date,
            metadata=metadata,
        )
        data = await self._http.post(_PATH, json=req.model_dump(exclude_none=True))
        return Invoice.model_validate(data)

    async def retrieve(self, invoice_id: str) -> Invoice:
        """Retrieve an invoice by ID (async).

        Args:
            invoice_id: The invoice ID.

        Returns:
            A :class:`~speedapi.models.Invoice`.
        """
        data = await self._http.get(f"{_PATH}/{invoice_id}")
        return Invoice.model_validate(data)

    async def list(
        self,
        *,
        limit: int = 20,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
    ) -> InvoiceList:
        """List invoices (async).

        Args:
            limit: Max invoices to return. Defaults to 20.
            starting_after: Forward pagination cursor.
            ending_before: Backward pagination cursor.

        Returns:
            A :class:`~speedapi.models.InvoiceList`.
        """
        params: Dict[str, Any] = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        data = await self._http.get(_PATH, params=params)
        return InvoiceList.model_validate(data)
