<div align="center">

# ⚡ speedapi-python

**The official Python SDK for the [Speed Merchant API](https://docs.tryspeed.com)**

[![PyPI version](https://img.shields.io/pypi/v/speedapi-python.svg?style=flat-square&color=blueviolet)](https://pypi.org/project/speedapi-python/)
[![Python Versions](https://img.shields.io/pypi/pyversions/speedapi-python.svg?style=flat-square)](https://pypi.org/project/speedapi-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Type Checked](https://img.shields.io/badge/type--checked-mypy-informational?style=flat-square)](https://mypy-lang.org/)

> Sync & async support · Pydantic v2 models · Full type hints · Webhook verification

</div>

---

## Features

- 🔄 **Sync & Async** clients powered by `httpx`
- 🧩 **Pydantic v2** request / response models with IDE autocomplete
- 🛡️ **Rich error hierarchy** — `AuthenticationError`, `RateLimitError`, `NotFoundError` and more
- 🔗 **Checkout Sessions**, **Invoices**, **Pay Requests**, **Balances**
- 🔒 **Webhook signature verification** (HMAC-SHA256 with replay protection)
- 🐍 Python 3.9+ with 100% type annotations

---

## Installation

```bash
pip install speedapi-python
```

---

## Quick Start

### Synchronous

```python
from speedapi import SpeedAPI

client = SpeedAPI(api_key="sk_live_...")

# Check balance
balance = client.balances.retrieve()
sats = client.balances.retrieve_sats()
print(f"Available: {sats} SATS")

# Create a checkout session
session = client.checkout_sessions.create(
    amount=5000,        # amount in cents (for USD)
    currency="USD",
    success_url="https://example.com/success",
    cancel_url="https://example.com/cancel",
    description="Premium subscription",
)
print(f"Redirect to: {session.url}")

# Create a Lightning pay request
pr = client.pay_requests.create(
    amount=21000,
    currency="SATS",
    description="Coffee ☕",
)
print(f"Pay via: {pr.lightning_invoice}")
```

### Asynchronous (async/await)

```python
import asyncio
from speedapi import AsyncSpeedAPI

async def main():
    async with AsyncSpeedAPI(api_key="sk_live_...") as client:
        # All resources work identically — just add await
        balance = await client.balances.retrieve()
        
        session = await client.checkout_sessions.create(
            amount=5000,
            currency="USD",
            success_url="https://example.com/success",
        )
        print(session.url)

asyncio.run(main())
```

### FastAPI Integration Example

```python
from fastapi import FastAPI, Request
from speedapi import AsyncSpeedAPI

app = FastAPI()
speed = AsyncSpeedAPI(api_key="sk_live_...")

@app.post("/create-session")
async def create_session():
    session = await speed.checkout_sessions.create(
        amount=999,
        currency="USD",
        success_url="https://myapp.com/success",
    )
    return {"checkout_url": session.url}
```

---

## API Reference

### `SpeedAPI` / `AsyncSpeedAPI`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | required | Your Speed secret key (`sk_live_...`) |
| `base_url` | `str` | `https://api.tryspeed.com` | API base URL |
| `timeout` | `float` | `30.0` | Request timeout in seconds |

### Resources

#### `client.balances`

| Method | Returns | Description |
|--------|---------|-------------|
| `retrieve()` | `Balance` | All available/pending balances |
| `retrieve_sats()` | `float` | Available SATS balance (convenience) |

#### `client.checkout_sessions`

| Method | Returns | Description |
|--------|---------|-------------|
| `create(amount, currency, ...)` | `CheckoutSession` | Create a hosted checkout page |
| `retrieve(session_id)` | `CheckoutSession` | Get a session by ID |
| `list(limit, ...)` | `CheckoutSessionList` | List sessions (paginated) |
| `expire(session_id)` | `CheckoutSession` | Expire an open session |

#### `client.invoices`

| Method | Returns | Description |
|--------|---------|-------------|
| `create(amount, currency, ...)` | `Invoice` | Create a new invoice |
| `retrieve(invoice_id)` | `Invoice` | Get an invoice by ID |
| `list(limit, ...)` | `InvoiceList` | List invoices (paginated) |

#### `client.pay_requests`

| Method | Returns | Description |
|--------|---------|-------------|
| `create(amount, currency, ...)` | `PayRequest` | Create a pay request (Lightning) |
| `retrieve(pay_request_id)` | `PayRequest` | Get a pay request by ID |
| `list(limit, ...)` | `PayRequestList` | List pay requests (paginated) |

---

## Error Handling

`speedapi-python` raises specific exceptions for every error class — no need to inspect raw status codes.

```python
from speedapi import (
    SpeedAPI,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIStatusError,
    APIConnectionError,
)

client = SpeedAPI(api_key="sk_live_...")

try:
    session = client.checkout_sessions.retrieve("cs_nonexistent")
except AuthenticationError:
    print("Invalid API key — check your credentials")
except NotFoundError:
    print("Session not found")
except RateLimitError:
    print("Too many requests — back off and retry")
except APIConnectionError as e:
    print(f"Network error: {e}")
except APIStatusError as e:
    print(f"Unexpected API error {e.status_code}: {e.response_body}")
```

### Exception Hierarchy

```
SpeedAPIError
├── AuthenticationError     # HTTP 401
├── PermissionDeniedError   # HTTP 403
├── NotFoundError           # HTTP 404
├── RateLimitError          # HTTP 429
├── APIStatusError          # other 4xx / 5xx (carries .status_code + .response_body)
└── APIConnectionError      # network-level (timeout, DNS, etc.)
```

---

## Webhook Verification

Speed signs every webhook with HMAC-SHA256. Always verify the signature before processing.

```python
from fastapi import FastAPI, Request, HTTPException
from speedapi.resources.webhooks import Webhooks, WebhookSignatureVerificationError

app = FastAPI()
WEBHOOK_SECRET = "whsec_..."   # from your Speed Dashboard

@app.post("/webhooks/speed")
async def speed_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Speed-Signature", "")

    try:
        event = Webhooks.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=WEBHOOK_SECRET,
        )
    except WebhookSignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event.type == "checkout_session.completed":
        session_id = event.data.get("object", {}).get("id")
        print(f"✅ Checkout completed: {session_id}")
    elif event.type == "invoice.paid":
        invoice_id = event.data.get("object", {}).get("id")
        print(f"💰 Invoice paid: {invoice_id}")

    return {"received": True}
```

> **Security**: The SDK automatically rejects webhooks older than 5 minutes to prevent replay attacks.

---

## Development

```bash
# Clone the repo
git clone https://github.com/furkankoykiran/speedapi_lib
cd speedapi_lib

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run the test suite
pytest tests/ -v --tb=short --cov=src/speedapi

# Type check
mypy src/speedapi
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ by <a href="https://github.com/furkankoykiran">Furkan Köykıran</a>
</div>