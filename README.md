# WebScraping — CI test runner

This repository contains a set of web-scraping experiments and small scripts in the `tests/` directory. I added a minimal CI workflow to run tests automatically on push and pull requests.

## What I added

- `requirements.txt` — pinned development/runtime dependencies.
- `tests/test_runner.py` — a pytest-based runner that executes each script in `tests/` as a separate process (this helps detect runtime errors in the scripts).
- `.github/workflows/python-tests.yml` — GitHub Actions to install dependencies and run `pytest` on pushes and PRs to `main`.

## Run tests locally

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tests with pytest:

```bash
python -m pytest -q
```

Note: The tests in `tests/` are small scripts which may perform network requests. Running them in CI depends on network availability and the remote resources.

## CI details

The CI workflow runs on pushes and PRs to `main`. It runs tests for Python 3.10 and 3.11, caches pip, and runs `pytest -q`.

If you want tests to be purely local (no external network calls), convert the scripts to unit tests with mocking for network I/O.
