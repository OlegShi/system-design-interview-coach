# System Design Interview Coach — Backend

Python / FastAPI backend that powers the AI-agent interview coaching workflow.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

## Quick start

```bash
cd backend

# Install dependencies
uv sync

# Run the dev server (auto-reload)
uv run uvicorn app.main:app --reload
# → listening on http://localhost:8000

# Or simply:
uv run python main.py
```

## API endpoints

| Method | Path                        | Description                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/health`                   | Health check                         |
| POST   | `/sessions`                 | Create & bootstrap a new session     |
| GET    | `/sessions`                 | List all sessions                    |
| GET    | `/sessions/{id}`            | Get a single session with timeline   |
| POST   | `/sessions/{id}/run`        | Run the next workflow step           |
| POST   | `/sessions/{id}/answers`    | Submit an answer for a task          |

## Architecture

```
app/
  api/          ← FastAPI route handlers (thin — delegates to workflow)
  agents/       ← Agent orchestrators (specifier, planner, task gen, scorer)
  skills/       ← Pure-logic modules called by agents
  workflow/     ← Execution order (bootstrap, runner)
  domain/       ← Pydantic models (Session, Event) + in-memory store
```

**Design rules:**

1. Agents orchestrate behaviour — they never contain business logic directly.
2. Skills hold the actual logic (scoring heuristics, task generation, etc.).
3. Workflow controls execution order; API only calls workflow.
4. Everything emits timeline events so the UI can render the full trace.

## Tests

```bash
uv run pytest
```

## Linting / type-checking

```bash
uv run ruff check .
uv run mypy app
```
