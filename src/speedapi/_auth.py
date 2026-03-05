"""Authentication helpers for the Speed API."""

from __future__ import annotations

import base64


def build_basic_auth_header(api_key: str) -> str:
    """Build an HTTP Basic Authentication header value from a Speed API key.

    Speed uses ``Basic <base64("api_key:")>`` authentication — note the
    trailing colon (empty password field per RFC 7617).

    Args:
        api_key: A Speed secret API key, e.g. ``sk_live_...``.

    Returns:
        The value to use in the ``Authorization`` HTTP header, e.g.
        ``"Basic c2tfbGl2ZV8uLi46"``.

    Example:
        >>> header_value = build_basic_auth_header("sk_live_abc123")
        >>> assert header_value.startswith("Basic ")
    """
    token = base64.b64encode(f"{api_key}:".encode("ascii")).decode("ascii")
    return f"Basic {token}"
