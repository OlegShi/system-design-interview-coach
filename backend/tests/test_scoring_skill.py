"""Tests for the scoring skill — the core heuristic scoring engine."""

from app.domain.models import Event, Session
from app.skills.scoring_skill import (
    _cross_answer_bonus,
    _generate_feedback,
    _keyword_score,
    _length_score,
    _score_answer,
    RUBRIC_KEYWORDS,
    score_session,
)


# ---------------------------------------------------------------------------
# _length_score
# ---------------------------------------------------------------------------

def test_length_score_empty():
    assert _length_score("") == 0
    assert _length_score("   ") == 0


def test_length_score_short():
    assert _length_score("Hello") == 1  # < 40 chars


def test_length_score_medium():
    assert _length_score("x" * 80) == 2  # 40-119


def test_length_score_long():
    assert _length_score("x" * 200) == 3  # >= 120


# ---------------------------------------------------------------------------
# _keyword_score
# ---------------------------------------------------------------------------

def test_keyword_score_no_matches():
    assert _keyword_score("random text", ["endpoint", "schema"]) == 0


def test_keyword_score_some_matches():
    text = "We add an endpoint for GET and POST with pagination"
    score = _keyword_score(text, RUBRIC_KEYWORDS["api_design"])
    assert score >= 3  # endpoint, get, post, pagination


def test_keyword_score_capped_at_5():
    # Hit every keyword in the list
    text = " ".join(RUBRIC_KEYWORDS["requirements"])
    assert _keyword_score(text, RUBRIC_KEYWORDS["requirements"]) == 5


# ---------------------------------------------------------------------------
# _score_answer
# ---------------------------------------------------------------------------

def test_score_answer_empty():
    assert _score_answer("", "requirements") == 0


def test_score_answer_short_no_keywords():
    assert _score_answer("Some short text", "requirements") == 1


def test_score_answer_detailed_with_keywords():
    answer = (
        "The system must handle functional requirements including user login, "
        "feed generation, and notifications. Non-functional requirements are "
        "latency p95 < 200ms, throughput > 10k QPS, high availability SLA of "
        "99.99%. Read/write ratio is expected to be 80/20 with 100M DAU."
    )
    score = _score_answer(answer, "requirements")
    assert score >= 4  # length 3 + keyword bonus


def test_score_answer_capped_at_5():
    answer = " ".join(RUBRIC_KEYWORDS["scalability"]) * 5
    assert _score_answer(answer, "scalability") == 5


# ---------------------------------------------------------------------------
# _cross_answer_bonus
# ---------------------------------------------------------------------------

def test_cross_answer_bonus_no_keywords():
    assert _cross_answer_bonus("nothing relevant here", "observability") == 0


def test_cross_answer_bonus_some_keywords():
    text = "we use prometheus metrics and grafana dashboards"
    bonus = _cross_answer_bonus(text, "observability")
    assert bonus >= 2


def test_cross_answer_bonus_many_keywords():
    text = "metrics logs tracing prometheus grafana alert dashboard"
    bonus = _cross_answer_bonus(text, "observability")
    assert bonus == 3


# ---------------------------------------------------------------------------
# _generate_feedback
# ---------------------------------------------------------------------------

def test_feedback_no_answers():
    scores = {k: 0 for k in RUBRIC_KEYWORDS}
    fb = _generate_feedback(scores, 0)
    assert "No answers submitted" in fb


def test_feedback_perfect_scores():
    scores = {k: 5 for k in RUBRIC_KEYWORDS}
    fb = _generate_feedback(scores, 6)
    assert "Excellent" in fb or "full marks" in fb


def test_feedback_mixed_scores():
    scores = {k: 0 for k in RUBRIC_KEYWORDS}
    scores["requirements"] = 5
    scores["api_design"] = 4
    fb = _generate_feedback(scores, 6)
    assert "Areas to strengthen" in fb
    assert "Strong areas" in fb


# ---------------------------------------------------------------------------
# score_session  (end-to-end)
# ---------------------------------------------------------------------------

def _make_session_with_answers(answers: dict[str, str]) -> Session:
    session = Session(title="Design a URL Shortener")
    for task_id, answer in answers.items():
        session.events.append(
            Event(
                type="answer_submitted",
                content=f"Answer for {task_id}",
                payload={"task_id": task_id, "answer": answer},
            )
        )
    return session


def test_score_session_no_answers():
    session = Session(title="Empty Session")
    result = score_session(session)
    assert result["answers_count"] == 0
    assert result["overall_score"] == 0
    assert result["max_score"] == 40  # 8 * 5
    assert "No answers submitted" in result["feedback"]


def test_score_session_with_answers():
    answers = {
        "requirements": (
            "Functional requirements: create short URL, redirect to long URL. "
            "Non-functional: latency under 100ms, availability 99.99%, DAU 10M."
        ),
        "api_design": (
            "POST /urls — request body with long URL, response with short code. "
            "GET /{code} — 301 redirect. Pagination for user's history. "
            "Rate limit per user: 100 req/min."
        ),
        "data_model": (
            "SQL table: urls (id PK, short_code UNIQUE INDEX, long_url, user_id FK, "
            "created_at). Partition by created_at for time-series queries."
        ),
    }
    session = _make_session_with_answers(answers)
    result = score_session(session)
    assert result["answers_count"] == 3
    assert result["rubric_scores"]["requirements"] >= 3
    assert result["rubric_scores"]["api_design"] >= 3
    assert result["rubric_scores"]["data_model"] >= 3
    assert "per_task_scores" in result


def test_score_session_observability_bonus():
    answers = {
        "reliability": (
            "We use prometheus metrics and grafana dashboards for monitoring. "
            "Circuit breakers with retries on transient failures. Health checks "
            "on every pod. OAuth and JWT for auth."
        ),
    }
    session = _make_session_with_answers(answers)
    result = score_session(session)
    # Should get cross-answer bonus for observability and security
    assert result["rubric_scores"]["observability"] >= 1
    assert result["rubric_scores"]["security"] >= 1


def test_score_session_uses_latest_answer():
    """When a task has multiple answers, only the latest is scored."""
    session = Session(title="Test")
    # first answer — short
    session.events.append(
        Event(
            type="answer_submitted",
            content="first",
            payload={"task_id": "requirements", "answer": "hi"},
        )
    )
    # second answer — detailed
    detailed = (
        "Functional and non-functional requirements including latency, "
        "throughput, availability SLA, DAU, read write ratio constraints."
    )
    session.events.append(
        Event(
            type="answer_submitted",
            content="second",
            payload={"task_id": "requirements", "answer": detailed},
        )
    )
    result = score_session(session)
    assert result["rubric_scores"]["requirements"] >= 3
