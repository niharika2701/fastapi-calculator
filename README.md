# FastAPI Calculator

A full-stack calculator built with FastAPI (Python), tested with unit,
integration, and end-to-end tests, and deployed with GitHub Actions CI.

---

## Project Structure
```
fastapi-calculator/
├── app/
│   ├── __init__.py
│   ├── main.py          ← FastAPI app, routes, logging
│   └── operations.py    ← Pure math functions
├── templates/
│   └── index.html       ← Calculator UI
├── tests/
│   ├── __init__.py
│   ├── test_operations.py  ← Unit tests
│   ├── test_main.py        ← Integration tests
│   └── test_e2e.py         ← End-to-end tests (Playwright)
├── .github/
│   └── workflows/
│       └── ci.yml       ← GitHub Actions CI pipeline
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Setup
```bash
# Clone the repo
git clone https://github.com/niharika2701/fastapi-calculator.git
cd fastapi-calculator

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium
```

---

## Run the App
```bash
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser.

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

| Method | Endpoint    | Description              |
|--------|-------------|--------------------------|
| GET    | `/`         | Calculator UI             |
| GET    | `/health`   | Health check              |
| GET    | `/docs`     | Interactive API docs      |
| POST   | `/add`      | Add two numbers           |
| POST   | `/subtract` | Subtract two numbers      |
| POST   | `/multiply` | Multiply two numbers      |
| POST   | `/divide`   | Divide two numbers        |
| POST   | `/power`    | Raise a to the power of b |
| POST   | `/modulo`   | Remainder of a divided by b |

All POST endpoints accept:
```json
{ "a": number, "b": number }
```

And return:
```json
{ "result": number }
```

---

## Running Tests
```bash
# Unit tests only
python -m pytest tests/test_operations.py -v

# Integration tests only
python -m pytest tests/test_main.py -v

# End-to-end tests (server must be running)
python -m pytest tests/test_e2e.py -v

# Watch the browser during E2E tests
python -m pytest tests/test_e2e.py -v --headed

# All tests at once
python -m pytest tests/test_operations.py tests/test_main.py tests/test_e2e.py -v
```

---

## Testing Approach

This project follows TDD (Test Driven Development) and the AAA pattern.

**TDD — Test Driven Development**
Tests were written before the implementation code.
- Red: write a failing test
- Green: write the minimum code to pass it
- Refactor: clean up

**AAA — Arrange, Act, Assert**
Every test follows three clear sections:
- Arrange: set up inputs
- Act: call the function or endpoint
- Assert: verify the result

**Three levels of testing:**

| Level       | File                  | What it tests                        |
|-------------|-----------------------|--------------------------------------|
| Unit        | test_operations.py    | Individual math functions            |
| Integration | test_main.py          | API endpoints and HTTP responses     |
| End-to-End  | test_e2e.py           | Real browser interactions via Playwright |

---

## Continuous Integration

GitHub Actions runs automatically on every push:

1. **Unit and Integration Tests** — fast, no browser required
2. **End-to-End Tests** — runs after job 1 passes, uses headless Chromium

Check the Actions tab on GitHub to see the latest run results.

---

## Logging

The application logs all operations and errors to:
- Terminal output (console)
- `calculator.log` file

Log levels used:
- `INFO` — successful operations
- `ERROR` — validation errors, division by zero, unexpected failures