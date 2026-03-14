"""Tests for the workflow layer (bootstrap + runner)."""

from app.domain.models import Session
from app.workflow.bootstrap import bootstrap_session
from app.workflow.runner import has_event, run_next_steps


# ---------------------------------------------------------------------------
# bootstrap_session
# ---------------------------------------------------------------------------

def test_bootstrap_adds_system_event():
    session = bootstrap_session(Session(title="Test"))
    types = [e.type for e in session.events]
    assert "system" in types


def test_bootstrap_runs_constitution():
    session = bootstrap_session(Session(title="Test"))
    types = [e.type for e in session.events]
    assert "constitution_started" in types
    assert "constitution_completed" in types


def test_bootstrap_runs_specifier():
    session = bootstrap_session(Session(title="Test"))
    types = [e.type for e in session.events]
    assert "specifier_agent_started" in types
    assert "specifier_agent_completed" in types


def test_bootstrap_runs_planner():
    session = bootstrap_session(Session(title="Test"))
    types = [e.type for e in session.events]
    assert "planner_agent_started" in types
    assert "planner_agent_completed" in types


def test_bootstrap_does_not_run_tasks_or_scorer():
    session = bootstrap_session(Session(title="Test"))
    types = [e.type for e in session.events]
    assert "task_generator_agent_completed" not in types
    assert "scorer_agent_completed" not in types


# ---------------------------------------------------------------------------
# has_event helper
# ---------------------------------------------------------------------------

def test_has_event_true():
    session = bootstrap_session(Session(title="Test"))
    assert has_event(session, "system") is True


def test_has_event_false():
    session = Session(title="Test")
    assert has_event(session, "nonexistent") is False


# ---------------------------------------------------------------------------
# run_next_steps
# ---------------------------------------------------------------------------

def test_runner_generates_tasks_first():
    session = bootstrap_session(Session(title="Runner Test"))
    session = run_next_steps(session)
    types = [e.type for e in session.events]
    assert "task_generator_agent_completed" in types
    assert "scorer_agent_completed" not in types


def test_runner_scores_after_tasks():
    session = bootstrap_session(Session(title="Runner Test"))
    session = run_next_steps(session)   # tasks
    session = run_next_steps(session)   # scoring
    types = [e.type for e in session.events]
    assert "scorer_agent_completed" in types


def test_runner_noop_when_complete():
    session = bootstrap_session(Session(title="Runner Test"))
    session = run_next_steps(session)   # tasks
    session = run_next_steps(session)   # scoring
    session = run_next_steps(session)   # noop
    types = [e.type for e in session.events]
    assert "run_noop" in types
