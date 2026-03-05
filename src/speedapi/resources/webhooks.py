"""Webhooks resource — HMAC-SHA256 signature verification and event construction."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

from speedapi.exceptions import SpeedAPIError
from speedapi.models import WebhookEvent

_DEFAULT_TOLERANCE_SECONDS = 300  # 5 minutes


class WebhookSignatureVerificationError(SpeedAPIError):
    """Raised when a webhook payload fails signature or timestamp verification.

    This is a subclass of :class:`~speedapi.exceptions.SpeedAPIError`.
    """


class Webhooks:
    """Webhook utilities for verifying Speed API event signatures.

    Speed signs webhook payloads using HMAC-SHA256 with your webhook secret
    and includes the signature in the ``Speed-Signature`` HTTP header.

    Example:
        >>> from speedapi.resources.webhooks import Webhooks
        >>> event = Webhooks.construct_event(
        ...     payload=request.body,
        ...     sig_header=request.headers["Speed-Signature"],
        ...     secret="whsec_...",
        ... )
        >>> print(event.type)
        'checkout_session.completed'
    """

    @staticmethod
    def construct_event(
        payload: bytes,
        sig_header: str,
        secret: str,
        *,
        tolerance: Optional[int] = _DEFAULT_TOLERANCE_SECONDS,
    ) -> WebhookEvent:
        """Verify a webhook signature and construct a :class:`~speedapi.models.WebhookEvent`.

        The ``Speed-Signature`` header has the format::

            t=<unix_timestamp>,v1=<hex_signature>

        Args:
            payload: The raw request body bytes received from Speed.
            sig_header: The value of the ``Speed-Signature`` HTTP header.
            secret: Your webhook endpoint secret (starts with ``whsec_``).
            tolerance: Maximum age of the webhook in seconds before rejection.
                Set to ``None`` to disable timestamp checking (not recommended
                in production). Defaults to 300 (5 minutes).

        Returns:
            A validated :class:`~speedapi.models.WebhookEvent` instance.

        Raises:
            WebhookSignatureVerificationError: If the signature is invalid,
                the timestamp is missing/malformed, or the event is outside
                the allowed ``tolerance`` window.

        Example:
            >>> event = Webhooks.construct_event(
            ...     payload=b'{"id":"evt_001","type":"invoice.paid","data":{}}',
            ...     sig_header="t=1700000000,v1=abc123...",
            ...     secret="whsec_test_secret",
            ... )
        """
        # --- Parse header ---
        parts = dict(item.split("=", 1) for item in sig_header.split(",") if "=" in item)
        timestamp_str = parts.get("t")
        received_sig = parts.get("v1")

        if not timestamp_str or not received_sig:
            raise WebhookSignatureVerificationError(
                "Malformed Speed-Signature header: missing 't' or 'v1' field.",
            )

        try:
            timestamp = int(timestamp_str)
        except ValueError:
            raise WebhookSignatureVerificationError(
                f"Malformed Speed-Signature header: timestamp '{timestamp_str}' is not an integer.",
            )

        # --- Timestamp tolerance check ---
        if tolerance is not None:
            current_time = int(time.time())
            if abs(current_time - timestamp) > tolerance:
                raise WebhookSignatureVerificationError(
                    f"Webhook timestamp is too old (age: {abs(current_time - timestamp)}s, "
                    f"tolerance: {tolerance}s). Possible replay attack.",
                )

        # --- Compute expected signature ---
        signed_payload = f"{timestamp}.".encode() + payload
        expected_sig = hmac.new(
            secret.encode("utf-8"),
            signed_payload,
            hashlib.sha256,
        ).hexdigest()

        # --- Constant-time comparison ---
        if not hmac.compare_digest(expected_sig, received_sig):
            raise WebhookSignatureVerificationError(
                "Speed-Signature verification failed. The payload may have been tampered with.",
            )

        # --- Deserialise ---
        import json  # local import to keep module-level imports clean

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise WebhookSignatureVerificationError(
                f"Webhook payload is not valid JSON: {exc}",
            ) from exc

        return WebhookEvent.model_validate(data)
