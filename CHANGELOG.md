# Changelog

All notable changes to `speedapi-python` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] — 2026-03-05

### ⚠️ Breaking Changes

This is a **complete rewrite**. The package is now published as `speedapi-python`
(was `speedapi-lib`) and the import path has changed from `speedapi_lib` to `speedapi`.

```python
# OLD (< 2.0)
from speedapi_lib.speedapi import SpeedAPI

# NEW (>= 2.0)
from speedapi import SpeedAPI
```

### Added

- **`src/` layout** — modern PEP 517 project structure with `pyproject.toml`
- **`SpeedAPI`** — fully typed synchronous client (replaces old class)
- **`AsyncSpeedAPI`** — new asynchronous client (`async/await`, powered by `httpx`)
- **Pydantic v2 models** — `CheckoutSession`, `Invoice`, `PayRequest`, `Balance`,
  `WebhookEvent` with full IDE autocomplete and validation
- **Custom exception hierarchy** — `AuthenticationError`, `PermissionDeniedError`,
  `NotFoundError`, `RateLimitError`, `APIStatusError`, `APIConnectionError`
- **Resource modules** — `checkout_sessions`, `invoices`, `pay_requests`, `balances`
- **Webhook verification** — HMAC-SHA256 signature validation with replay-attack protection
- **Google-style docstrings** on every public function and class
- **54 unit tests** with `respx` HTTP mocking (100% resources covered)
- **GitHub Actions CI** — lint (ruff), type-check (mypy), pytest on Python 3.9–3.12
- **GitHub Actions publish** — PyPI Trusted Publisher (OIDC), no secrets required
- Community standards: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  issue templates, PR template

### Changed

- HTTP client: `requests` → `httpx`
- Python requirement: `>=3.7` → `>=3.9`
- Dependency: removed `bolt11` (no longer needed for core SDK)

### Removed

- `SpeedAPI.pay_invoice()` — Lightning Network payment sending is now out of scope
  for the core SDK; use the Pay Requests resource instead
- `SpeedAPI.get_invoice_info()` — superseded by `client.invoices.retrieve()`
- `SpeedAPI.get_balance_sats()` — use `client.balances.retrieve_sats()` instead

---

## [0.1.4] — 2024-09-01 *(legacy)*

- Initial public release with `requests`-based client
- `get_balance_sats()`, `pay_invoice()`, `get_invoice_info()`

[2.0.0]: https://github.com/furkankoykiran/speedapi_lib/releases/tag/v2.0.0
[0.1.4]: https://github.com/furkankoykiran/speedapi_lib/releases/tag/v0.1.4
