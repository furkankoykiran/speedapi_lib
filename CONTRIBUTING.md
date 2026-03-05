# Contributing to speedapi-python

Thank you for your interest in contributing! This document will help you get
started quickly and submit high-quality pull requests.

---

## Table of Contents

- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Type Checking](#type-checking)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Versioning](#versioning)

---

## Development Setup

Clone the repository and install in editable mode with all dev dependencies:

```bash
git clone https://github.com/furkankoykiran/speedapi_lib.git
cd speedapi_lib
pip install -e ".[dev]"
```

We strongly recommend working inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Running Tests

```bash
# Run the full test suite
pytest tests/ -v --tb=short

# With coverage report
pytest tests/ -v --cov=src/speedapi --cov-report=term-missing
```

All pull requests must keep **every existing test green** and should add tests
for any new behaviour. We use `respx` to mock `httpx` calls — no real network
requests are made during tests.

---

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Run it
before committing:

```bash
ruff check src/ tests/          # lint
ruff format src/ tests/         # auto-format
```

The CI pipeline will fail if `ruff check` reports any errors.

**Key conventions:**

- **Line length**: 100 characters
- **Imports**: `isort`-compatible ordering (Ruff handles this)
- **Docstrings**: [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings),
  mandatory for all public functions, methods, and classes
- **Type hints**: required on all function signatures

---

## Type Checking

```bash
mypy src/speedapi --ignore-missing-imports
```

All public APIs must be fully type-annotated. `mypy --strict` should produce no
errors on `src/speedapi/`.

---

## Submitting a Pull Request

1. **Fork** the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. **Make your changes** — keep commits focused and atomic.

3. **Run all checks locally**:
   ```bash
   ruff check src/ tests/
   mypy src/speedapi --ignore-missing-imports
   pytest tests/ -v
   ```

4. **Update `CHANGELOG.md`** under the `[Unreleased]` section.

5. **Open a pull request** against the `main` branch. Fill in the PR template.

### PR Acceptance Criteria

| Criterion | Requirement |
|-----------|-------------|
| Tests | All existing tests pass; new tests added for new behaviour |
| Lint | `ruff check` passes with no errors |
| Types | `mypy` passes with no errors |
| Docs | Public API has Google-style docstrings |
| Changelog | `CHANGELOG.md` updated |

---

## Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** — incompatible API changes
- **MINOR** — new backwards-compatible functionality
- **PATCH** — backwards-compatible bug fixes

Versions are managed via `pyproject.toml`. A GitHub Actions workflow
(`publish.yml`) automatically publishes to PyPI when a `v*.*.*` tag is pushed.

---

## Questions?

Open a [GitHub Discussion](https://github.com/furkankoykiran/speedapi_lib/discussions)
or a [GitHub Issue](https://github.com/furkankoykiran/speedapi_lib/issues).
