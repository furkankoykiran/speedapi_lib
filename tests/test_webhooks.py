"""Unit tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac
import json
import time

import pytest

from speedapi.resources.webhooks import Webhooks, WebhookSignatureVerificationError

SECRET = "whsec_test_super_secret"
PAYLOAD_DICT = {
    "id": "evt_001",
    "type": "checkout_session.completed",
    "created": 1700000000,
    "data": {"object": {"id": "cs_001"}},
    "livemode": True,
}
PAYLOAD_BYTES = json.dumps(PAYLOAD_DICT).encode()


def _make_sig_header(payload: bytes, secret: str, timestamp: int) -> str:
    signed = f"{timestamp}.".encode() + payload
    sig = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={sig}"


class TestWebhookConstuctEvent:
    def test_valid_signature_returns_event(self):
        ts = int(time.time())
        header = _make_sig_header(PAYLOAD_BYTES, SECRET, ts)
        event = Webhooks.construct_event(
            payload=PAYLOAD_BYTES, sig_header=header, secret=SECRET
        )
        assert event.id == "evt_001"
        assert event.type == "checkout_session.completed"
        assert event.data["object"]["id"] == "cs_001"

    def test_tampered_payload_raises(self):
        ts = int(time.time())
        header = _make_sig_header(PAYLOAD_BYTES, SECRET, ts)
        tampered = PAYLOAD_BYTES + b" extra"
        with pytest.raises(WebhookSignatureVerificationError, match="verification failed"):
            Webhooks.construct_event(payload=tampered, sig_header=header, secret=SECRET)

    def test_wrong_secret_raises(self):
        ts = int(time.time())
        header = _make_sig_header(PAYLOAD_BYTES, "wrong_secret", ts)
        with pytest.raises(WebhookSignatureVerificationError):
            Webhooks.construct_event(payload=PAYLOAD_BYTES, sig_header=header, secret=SECRET)

    def test_old_timestamp_raises_within_tolerance(self):
        old_ts = int(time.time()) - 400  # older than 300s default
        header = _make_sig_header(PAYLOAD_BYTES, SECRET, old_ts)
        with pytest.raises(WebhookSignatureVerificationError, match="too old"):
            Webhooks.construct_event(payload=PAYLOAD_BYTES, sig_header=header, secret=SECRET)

    def test_old_timestamp_allowed_without_tolerance(self):
        old_ts = 1000  # ancient timestamp
        header = _make_sig_header(PAYLOAD_BYTES, SECRET, old_ts)
        event = Webhooks.construct_event(
            payload=PAYLOAD_BYTES, sig_header=header, secret=SECRET, tolerance=None
        )
        assert event.id == "evt_001"

    def test_malformed_header_raises(self):
        with pytest.raises(WebhookSignatureVerificationError, match="Malformed"):
            Webhooks.construct_event(
                payload=PAYLOAD_BYTES, sig_header="garbage", secret=SECRET
            )

    def test_invalid_json_payload_raises(self):
        ts = int(time.time())
        bad_payload = b"not json"
        header = _make_sig_header(bad_payload, SECRET, ts)
        with pytest.raises(WebhookSignatureVerificationError, match="valid JSON"):
            Webhooks.construct_event(
                payload=bad_payload, sig_header=header, secret=SECRET, tolerance=None
            )
