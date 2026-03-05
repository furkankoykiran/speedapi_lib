"""Pydantic v2 models for Speed API request and response objects."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class Currency(str, Enum):
    """Supported payment currencies."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    SATS = "SATS"
    BTC = "BTC"


class CheckoutSessionStatus(str, Enum):
    """Lifecycle states of a checkout session."""

    OPEN = "open"
    COMPLETE = "complete"
    EXPIRED = "expired"


class InvoiceStatus(str, Enum):
    """Lifecycle states of an invoice."""

    OPEN = "open"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class PayRequestStatus(str, Enum):
    """Lifecycle states of a pay request."""

    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELED = "canceled"


class WebhookEventType(str, Enum):
    """Known Speed API webhook event types."""

    CHECKOUT_SESSION_COMPLETED = "checkout_session.completed"
    CHECKOUT_SESSION_EXPIRED = "checkout_session.expired"
    INVOICE_PAID = "invoice.paid"
    INVOICE_VOID = "invoice.void"
    PAY_REQUEST_PAID = "pay_request.paid"
    PAY_REQUEST_EXPIRED = "pay_request.expired"


# ---------------------------------------------------------------------------
# Shared / helper models
# ---------------------------------------------------------------------------


class APIModel(BaseModel):
    """Base model with common config for all Speed API objects."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="allow",  # forward-compatible with API additions
    )


class BalanceItem(APIModel):
    """A single balance entry for one currency.

    Attributes:
        amount: Balance amount in the smallest unit (sats, cents, etc.).
        target_currency: ISO currency code or "SATS"/"BTC".
    """

    amount: float
    target_currency: str


class Balance(APIModel):
    """Merchant balance response.

    Attributes:
        available: List of available balance items per currency.
        pending: List of pending balance items per currency.
    """

    available: List[BalanceItem] = Field(default_factory=list)
    pending: List[BalanceItem] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Checkout Sessions
# ---------------------------------------------------------------------------


class CreateCheckoutSessionRequest(APIModel):
    """Parameters for creating a new checkout session.

    Attributes:
        amount: Amount to charge in the smallest unit of ``currency``.
        currency: Three-letter ISO currency code or "SATS".
        success_url: URL to redirect the customer after successful payment.
        cancel_url: URL to redirect the customer if they cancel.
        description: Optional human-readable description shown on the checkout page.
        metadata: Optional key-value pairs you can attach for your own use.
    """

    amount: int
    currency: Currency = Currency.USD
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CheckoutSession(APIModel):
    """A Speed API checkout session object.

    Attributes:
        id: Unique identifier for the session.
        status: Current lifecycle state.
        amount: Amount in the smallest unit of ``currency``.
        currency: Payment currency.
        url: Hosted checkout page URL to redirect the customer to.
        success_url: Redirect URL on success.
        cancel_url: Redirect URL on cancel.
        description: Session description.
        metadata: Arbitrary key-value pairs.
        created_at: ISO 8601 creation timestamp.
        expires_at: ISO 8601 expiry timestamp.
    """

    id: str
    status: CheckoutSessionStatus = CheckoutSessionStatus.OPEN
    amount: int
    currency: str
    url: Optional[str] = None
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class CheckoutSessionList(APIModel):
    """Paginated list of checkout sessions.

    Attributes:
        data: List of checkout session objects.
        has_more: Whether additional pages exist.
    """

    data: List[CheckoutSession] = Field(default_factory=list)
    has_more: bool = False


# ---------------------------------------------------------------------------
# Invoices
# ---------------------------------------------------------------------------


class CreateInvoiceRequest(APIModel):
    """Parameters for creating a new invoice.

    Attributes:
        amount: Amount in the smallest unit of ``currency``.
        currency: Three-letter ISO currency code or "SATS".
        description: Human-readable description of the invoice.
        customer_email: Optional customer email to send the invoice to.
        due_date: Optional ISO 8601 due date.
        metadata: Optional key-value pairs.
    """

    amount: int
    currency: Currency = Currency.USD
    description: Optional[str] = None
    customer_email: Optional[str] = None
    due_date: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Invoice(APIModel):
    """A Speed API invoice object.

    Attributes:
        id: Unique identifier.
        status: Current lifecycle state.
        amount: Amount in the smallest unit of ``currency``.
        currency: Payment currency.
        description: Invoice description.
        customer_email: Customer email address.
        due_date: ISO 8601 due date.
        hosted_invoice_url: URL to view / pay the invoice.
        metadata: Arbitrary key-value pairs.
        created_at: ISO 8601 creation timestamp.
    """

    id: str
    status: InvoiceStatus = InvoiceStatus.OPEN
    amount: int
    currency: str
    description: Optional[str] = None
    customer_email: Optional[str] = None
    due_date: Optional[str] = None
    hosted_invoice_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class InvoiceList(APIModel):
    """Paginated list of invoices."""

    data: List[Invoice] = Field(default_factory=list)
    has_more: bool = False


# ---------------------------------------------------------------------------
# Pay Requests
# ---------------------------------------------------------------------------


class CreatePayRequestRequest(APIModel):
    """Parameters for creating a new pay request.

    Attributes:
        amount: Amount in the smallest unit of ``currency``.
        currency: Three-letter ISO currency code or "SATS".
        description: Human-readable description.
        expires_in: Seconds until the pay request expires.
        metadata: Optional key-value pairs.
    """

    amount: int
    currency: Currency = Currency.USD
    description: Optional[str] = None
    expires_in: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class PayRequest(APIModel):
    """A Speed API pay request object.

    Attributes:
        id: Unique identifier.
        status: Current lifecycle state.
        amount: Amount in the smallest unit of ``currency``.
        currency: Payment currency.
        description: Pay request description.
        payment_url: URL for the payer to complete the payment.
        lightning_invoice: Optional BOLT11 Lightning invoice string.
        metadata: Arbitrary key-value pairs.
        created_at: ISO 8601 creation timestamp.
        expires_at: ISO 8601 expiry timestamp.
    """

    id: str
    status: PayRequestStatus = PayRequestStatus.PENDING
    amount: int
    currency: str
    description: Optional[str] = None
    payment_url: Optional[str] = None
    lightning_invoice: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class PayRequestList(APIModel):
    """Paginated list of pay requests."""

    data: List[PayRequest] = Field(default_factory=list)
    has_more: bool = False


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


class WebhookEvent(APIModel):
    """A Speed API webhook event envelope.

    Attributes:
        id: Unique event identifier.
        type: Event type string (e.g. "checkout_session.completed").
        created: Unix timestamp when the event was created.
        data: Raw event payload dict (object-specific structure).
        livemode: ``True`` for production events.
    """

    id: str
    type: str
    created: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    livemode: bool = True
