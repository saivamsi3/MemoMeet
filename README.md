# MemoMeet

MemoMeet is an AI-powered meeting intelligence app built with Flask.

## Phase 1 Scope

Phase 1 delivers the project foundation and authentication layer:

- Flask app factory setup
- SQLite database via Flask-SQLAlchemy
- User registration, login, logout
- Password hashing and session management (Flask-Login)
- Protected dashboard route
- Base responsive layout with navbar, sidebar, footer, and theme toggle

## Quick Start

1. Create and sync environment:

```bash
uv sync
```

2. Configure environment variables:

```bash
cp .env.example .env
```

3. Run the app:

```bash
uv run main.py
```

4. Open:

```text
http://127.0.0.1:5000
```

## Run Core Tests

```bash
uv run pytest -q tests/test_auth.py tests/test_participants.py tests/test_meetings.py
```
