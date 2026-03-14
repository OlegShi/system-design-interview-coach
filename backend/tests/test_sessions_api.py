"""Tests for API endpoints (sessions CRUD + workflow)."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# POST /sessions — create & bootstrap
# ---------------------------------------------------------------------------

def test_create_session():
    r = client.post("/sessions", json={"title": "Design a Rate Limiter"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Design a Rate Limiter"
    assert "id" in data
    assert "events" in data
    # bootstrap should have produced at least constitution + specifier + planner events
    types = [e["type"] for e in data["events"]]
    assert "system" in types
    assert "constitution_completed" in types
    assert "specifier_agent_completed" in types
    assert "planner_agent_completed" in types


def test_create_session_missing_title():
    r = client.post("/sessions", json={})
    assert r.status_code == 422  # validation error


# ---------------------------------------------------------------------------
# GET /sessions — list
# ---------------------------------------------------------------------------

def test_list_sessions():
    # create one to make sure the list is non-empty
    client.post("/sessions", json={"title": "List Test"})
    r = client.get("/sessions")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1


# ---------------------------------------------------------------------------
# GET /sessions/{id} — detail
# ---------------------------------------------------------------------------

def test_get_session_by_id():
    create = client.post("/sessions", json={"title": "Detail Test"})
    sid = create.json()["id"]
    r = client.get(f"/sessions/{sid}")
    assert r.status_code == 200
    assert r.json()["id"] == sid


def test_get_session_not_found():
    r = client.get("/sessions/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# POST /sessions/{id}/run — step runner
# ---------------------------------------------------------------------------

def test_run_generates_tasks():
    create = client.post("/sessions", json={"title": "Run Test"})
    sid = create.json()["id"]

    r = client.post(f"/sessions/{sid}/run")
    assert r.status_code == 200
    types = [e["type"] for e in r.json()["events"]]
    assert "task_generator_agent_completed" in types


def test_run_scores_after_tasks():
    create = client.post("/sessions", json={"title": "Score Test"})
    sid = create.json()["id"]

    # first run → tasks
    client.post(f"/sessions/{sid}/run")
    # second run → scoring
    r = client.post(f"/sessions/{sid}/run")
    assert r.status_code == 200
    types = [e["type"] for e in r.json()["events"]]
    assert "scorer_agent_completed" in types


def test_run_noop_when_complete():
    create = client.post("/sessions", json={"title": "Noop Test"})
    sid = create.json()["id"]

    client.post(f"/sessions/{sid}/run")  # tasks
    client.post(f"/sessions/{sid}/run")  # scoring
    r = client.post(f"/sessions/{sid}/run")  # noop
    assert r.status_code == 200
    types = [e["type"] for e in r.json()["events"]]
    assert "run_noop" in types


# ---------------------------------------------------------------------------
# POST /sessions/{id}/answers — submit answer
# ---------------------------------------------------------------------------

def test_submit_answer():
    create = client.post("/sessions", json={"title": "Answer Test"})
    sid = create.json()["id"]

    r = client.post(
        f"/sessions/{sid}/answers",
        json={"task_id": "requirements", "answer": "functional and non-functional reqs"},
    )
    assert r.status_code == 200
    events = r.json()["events"]
    answer_events = [e for e in events if e["type"] == "answer_submitted"]
    assert len(answer_events) == 1
    assert answer_events[0]["payload"]["task_id"] == "requirements"


def test_submit_answer_not_found():
    r = client.post(
        "/sessions/00000000-0000-0000-0000-000000000000/answers",
        json={"task_id": "x", "answer": "y"},
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Full flow: create → tasks → answer → score
# ---------------------------------------------------------------------------

def test_full_flow():
    # 1. Create session
    create = client.post("/sessions", json={"title": "Design a URL Shortener"})
    sid = create.json()["id"]

    # 2. Generate tasks
    client.post(f"/sessions/{sid}/run")

    # 3. Submit answers
    client.post(
        f"/sessions/{sid}/answers",
        json={
            "task_id": "requirements",
            "answer": (
                "Functional: shorten URL, redirect. Non-functional: "
                "latency < 100ms, availability 99.99%, 10M DAU read/write."
            ),
        },
    )
    client.post(
        f"/sessions/{sid}/answers",
        json={
            "task_id": "api_design",
            "answer": (
                "POST /urls endpoint with request body and response schema. "
                "GET /{code} for redirect with 301 status code. Rate limit."
            ),
        },
    )

    # 4. Score
    r = client.post(f"/sessions/{sid}/run")
    data = r.json()

    # Find scorer payload
    scorer_events = [e for e in data["events"] if e["type"] == "scorer_agent_completed"]
    assert len(scorer_events) == 1
    payload = scorer_events[0]["payload"]

    assert payload["answers_count"] == 2
    assert payload["overall_score"] > 0
    assert payload["rubric_scores"]["requirements"] >= 3
    assert payload["rubric_scores"]["api_design"] >= 3
    assert "feedback" in payload
    assert "per_task_scores" in payload
