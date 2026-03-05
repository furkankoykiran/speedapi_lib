"""Core HTTP transport layer — synchronous and asynchronous httpx wrappers."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from speedapi._auth import build_basic_auth_header
from speedapi.exceptions import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

DEFAULT_BASE_URL = "https://api.tryspeed.com"
DEFAULT_TIMEOUT = 30.0


def _raise_for_status(response: httpx.Response) -> None:
    """Convert an HTTP error response into the appropriate SDK exception.

    Args:
        response: The :class:`httpx.Response` to inspect.

    Raises:
        AuthenticationError: On HTTP 401.
        PermissionDeniedError: On HTTP 403.
        NotFoundError: On HTTP 404.
        RateLimitError: On HTTP 429.
        APIStatusError: On any other 4xx / 5xx response.
    """
    if response.is_success:
        return

    body: str = response.text
    status = response.status_code

    common_kwargs: Dict[str, Any] = {"status_code": status, "response_body": body}

    if status == 401:
        raise AuthenticationError(
            "Authentication failed. Check your API key.", **common_kwargs
        )
    if status == 403:
        raise PermissionDeniedError(
            "Your API key does not have permission to perform this action.",
            **common_kwargs,
        )
    if status == 404:
        raise NotFoundError("The requested resource was not found.", **common_kwargs)
    if status == 429:
        raise RateLimitError(
            "Rate limit exceeded. Back off before retrying.", **common_kwargs
        )
    raise APIStatusError(
        f"API error {status}: {body}", **common_kwargs
    )


class SyncTransport:
    """Synchronous HTTP transport backed by :class:`httpx.Client`.

    Args:
        api_key: Speed secret API key (``sk_live_...``).
        base_url: Override the default Speed API base URL.
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "Authorization": build_basic_auth_header(api_key),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Speed-Version": "2024-04-24",
        }
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=self._headers,
            timeout=timeout,
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request.

        Args:
            path: API path relative to base URL.
            params: Optional query parameters.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = self._client.get(path, params=params)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a POST request.

        Args:
            path: API path relative to base URL.
            json: Request body to serialise as JSON.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = self._client.post(path, json=json)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    def delete(self, path: str) -> Any:
        """Send a DELETE request.

        Args:
            path: API path relative to base URL.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = self._client.delete(path)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> SyncTransport:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncTransport:
    """Asynchronous HTTP transport backed by :class:`httpx.AsyncClient`.

    Args:
        api_key: Speed secret API key (``sk_live_...``).
        base_url: Override the default Speed API base URL.
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "Authorization": build_basic_auth_header(api_key),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Speed-Version": "2024-04-24",
        }
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=timeout,
        )

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send an async GET request.

        Args:
            path: API path relative to base URL.
            params: Optional query parameters.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = await self._client.get(path, params=params)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send an async POST request.

        Args:
            path: API path relative to base URL.
            json: Request body to serialise as JSON.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = await self._client.post(path, json=json)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    async def delete(self, path: str) -> Any:
        """Send an async DELETE request.

        Args:
            path: API path relative to base URL.

        Returns:
            Decoded JSON response as a Python object.
        """
        try:
            resp = await self._client.delete(path)
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Network error: {exc}") from exc
        _raise_for_status(resp)
        return resp.json()

    async def aclose(self) -> None:
        """Close the underlying async HTTP connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTransport:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
