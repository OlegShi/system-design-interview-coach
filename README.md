# System Design Interview Coach

An AI-powered coaching tool that guides candidates through system design interviews using a multi-agent architecture, event-driven timeline, and structured rubric scoring.

---

## Demo Flow

1. **Create a session** — pick a problem (e.g. *"Design a Rate Limiter"*)
2. **Bootstrap** runs automatically — constitution → specifier agent → planner agent
3. **Generate tasks** — click *Run Session* to produce structured interview questions
4. **Answer tasks** — write responses in each task card and submit
5. **Score** — click *Run Session* again to evaluate answers against an 8-category rubric
6. **Review feedback** — see per-category scores, bar charts, and improvement suggestions

---

## Architecture

```
┌────────────────────────────────┐      ┌──────────────────────────┐
│         Next.js (UI)           │◄────►│     FastAPI (Backend)    │
│  Timeline · Task Cards · Dash  │ REST │  Agents · Skills · Store │
└────────────────────────────────┘      └──────────────────────────┘
```

### Backend layers

```
app/
  api/          → Route handlers (thin — delegates to workflow)
  agents/       → Agent orchestrators (specifier, planner, task gen, scorer)
  skills/       → Pure-logic modules called by agents
  workflow/     → Execution order (bootstrap, runner)
  domain/       → Pydantic models (Session, Event) + in-memory store
```

### Design principles

| # | Principle |
|---|-----------|
| 1 | Agents orchestrate behaviour — they never contain business logic directly |
| 2 | Skills hold the actual logic (scoring heuristics, task generation, etc.) |
| 3 | Workflow controls execution order; API only calls workflow |
| 4 | Everything emits timeline events so the UI can render the full trace |

### Agent pipeline

```
Session Created
  → Constitution (principles + rubric definition)
  → Specifier Agent (problem statement, assumptions, NFRs)
  → Planner Agent (architecture outline, components)
  ─── user clicks Run ───
  → Task Generator Agent (6 structured interview questions)
  ─── user submits answers, clicks Run ───
  → Scorer Agent (8-category rubric scoring + feedback)
```

### Rubric categories

| Category | Source |
|----------|--------|
| Requirements | Dedicated task |
| API Design | Dedicated task |
| Data Model | Dedicated task |
| Scalability | Dedicated task |
| Reliability | Dedicated task |
| Tradeoffs | Dedicated task |
| Observability | Cross-answer keyword detection |
| Security | Cross-answer keyword detection |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12+, FastAPI, Pydantic, uvicorn |
| Package manager | uv |
| Frontend | Next.js 16 (App Router), React 19, Tailwind CSS v4 |
| Testing | pytest, httpx |
| Linting | Ruff, ESLint, mypy |

---

## Getting Started

### Prerequisites

- **Python 3.12+** and [uv](https://docs.astral.sh/uv/)
- **Node.js 18+** and npm

### 1. Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**.

### 2. Frontend

In a separate terminal:

```bash
cd ui
npm install
npm run dev
```

The app will be available at **http://localhost:3000**.

### 3. Open in browser

| URL | What |
|-----|------|
| http://localhost:3000 | Main app |
| http://localhost:3000/sessions | Session list |
| http://localhost:8000/docs | Swagger API docs |
| http://localhost:8000/health | Health check |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/sessions` | Create & bootstrap a new session |
| `GET` | `/sessions` | List all sessions |
| `GET` | `/sessions/{id}` | Get a session with full timeline |
| `POST` | `/sessions/{id}/run` | Run the next workflow step |
| `POST` | `/sessions/{id}/answers` | Submit an answer for a task |

---

## Tests

```bash
cd backend
uv run pytest -v
```

---

## Project Structure

```
system-design-interview-coach/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── sessions.py          # FastAPI route handlers
│   │   ├── agents/
│   │   │   ├── specifier_agent.py    # Problem specification
│   │   │   ├── planner_agent.py      # Architecture planning
│   │   │   ├── task_generator_agent.py # Interview task generation
│   │   │   ├── scorer_agent.py       # Rubric scoring
│   │   │   └── agent_loader.py       # Instruction file loader
│   │   ├── skills/
│   │   │   ├── assumptions_skill.py  # Traffic assumptions
│   │   │   ├── plan_skill.py         # Plan outline generation
│   │   │   ├── task_skill.py         # Task question generation
│   │   │   └── scoring_skill.py      # Heuristic rubric scoring
│   │   ├── workflow/
│   │   │   ├── bootstrap.py          # Session bootstrap sequence
│   │   │   └── runner.py             # Step-by-step executor
│   │   └── domain/
│   │       ├── models.py             # Session & Event models
│   │       └── store.py              # In-memory session store
│   └── tests/
│       ├── test_health.py
│       ├── test_scoring_skill.py
│       ├── test_task_skill.py
│       ├── test_sessions_api.py
│       └── test_workflow.py
├── ui/
│   └── app/
│       ├── page.tsx                  # Landing page
│       ├── layout.tsx                # Root layout + nav
│       └── sessions/
│           ├── page.tsx              # Session list + create
│           └── [id]/
│               └── page.tsx          # Timeline, tasks, scoring dashboard
└── README.md
```

---

## Future Improvements

- **LLM-powered agents** — replace deterministic stubs with OpenAI / Anthropic calls
- **Persistent storage** — swap in-memory store for PostgreSQL or SQLite
- **Adaptive tasks** — generate follow-up questions based on answer quality
- **Real-time updates** — SSE or WebSocket for live agent progress
- **More test coverage** — frontend component tests, integration tests
- **Authentication** — user accounts and session history

---
