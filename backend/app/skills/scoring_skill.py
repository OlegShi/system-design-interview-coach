from typing import Any, Dict, List, Tuple

from app.domain.models import Session


# ---------------------------------------------------------------------------
# Map each generated task id → rubric category
# (mirrors task ids from task_skill.generate_interview_tasks)
# ---------------------------------------------------------------------------
TASK_TO_RUBRIC: Dict[str, str] = {
    "requirements": "requirements",
    "api_design": "api_design",
    "data_model": "data_model",
    "scaling": "scalability",
    "reliability": "reliability",
    "tradeoffs": "tradeoffs",
}

# ---------------------------------------------------------------------------
# Domain keywords used for heuristic scoring per rubric category.
# Each keyword match adds 1 point (capped at 5).
# ---------------------------------------------------------------------------
RUBRIC_KEYWORDS: Dict[str, List[str]] = {
    "requirements": [
        "functional", "non-functional", "use case", "user story",
        "latency", "throughput", "availability", "dau", "mau",
        "read", "write", "constraint", "sla", "slo",
    ],
    "api_design": [
        "endpoint", "rest", "grpc", "graphql", "request", "response",
        "get", "post", "put", "delete", "pagination", "schema",
        "idempoten", "rate limit", "versioning", "status code",
    ],
    "data_model": [
        "table", "schema", "column", "primary key", "foreign key",
        "index", "partition", "sql", "nosql", "document", "relation",
        "entity", "normali", "denormali", "blob", "time-series",
    ],
    "scalability": [
        "shard", "partition", "replica", "horizontal", "vertical",
        "cache", "cdn", "load balancer", "queue", "async",
        "throughput", "bottleneck", "scale out", "auto-scal",
    ],
    "reliability": [
        "retry", "circuit breaker", "failover", "replication",
        "backup", "recovery", "health check", "heartbeat",
        "redundan", "timeout", "dead letter", "idempoten", "graceful",
    ],
    "observability": [
        "metric", "log", "trace", "tracing", "prometheus", "grafana",
        "alert", "dashboard", "slo", "sli", "percentile", "p99",
        "monitor", "observ", "opentelemetry", "datadog",
    ],
    "security": [
        "auth", "oauth", "jwt", "token", "encryption", "tls", "https",
        "pii", "rbac", "permission", "acl", "firewall", "waf",
        "sanitiz", "injection", "cors", "secret",
    ],
    "tradeoffs": [
        "tradeoff", "trade-off", "consistency", "cap theorem",
        "eventual", "strong consistency", "latency", "cost",
        "complexity", "availability", "partition tolerance",
        "write-ahead", "optimistic", "pessimistic",
    ],
}

# Friendly labels for feedback messages
RUBRIC_LABELS: Dict[str, str] = {
    "requirements": "Requirements & Constraints",
    "api_design": "API Design",
    "data_model": "Data Model",
    "scalability": "Scalability",
    "reliability": "Reliability & Failure Handling",
    "observability": "Observability",
    "security": "Security & Privacy",
    "tradeoffs": "Tradeoffs",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _length_score(text: str) -> int:
    """Base score derived from answer length (0-3)."""
    n = len(text.strip())
    if n == 0:
        return 0
    if n < 40:
        return 1
    if n < 120:
        return 2
    return 3


def _keyword_score(text: str, keywords: List[str]) -> int:
    """Count distinct keyword hits in *text* (0-5)."""
    lower = text.lower()
    hits = sum(1 for kw in keywords if kw in lower)
    return min(hits, 5)


def _score_answer(text: str, rubric_key: str) -> int:
    """
    Deterministic heuristic score (0-5) for a single answer.

    Combines:
      • length score  (0-3) — rewards depth
      • keyword score (0-5) — rewards domain coverage

    Final = min(length + keyword_bonus, 5)
    """
    if not text.strip():
        return 0
    base = _length_score(text)
    kw = _keyword_score(text, RUBRIC_KEYWORDS.get(rubric_key, []))
    # keyword bonus: up to +2 on top of length score
    bonus = min(kw, 2)
    return min(base + bonus, 5)


def _collect_latest_answers(session: Session) -> Dict[str, str]:
    """Return the most recent answer text for each task_id."""
    latest: Dict[str, str] = {}
    for event in session.events:
        if event.type == "answer_submitted" and event.payload:
            task_id = str(event.payload.get("task_id", ""))
            answer = str(event.payload.get("answer", ""))
            if task_id:
                latest[task_id] = answer
    return latest


def _cross_answer_bonus(combined: str, rubric_key: str) -> int:
    """
    Award bonus points when any answer mentions keywords for rubric
    categories that have no dedicated task (observability, security).
    Returns a score floor (0–3) based on keyword density.
    """
    kw = _keyword_score(combined, RUBRIC_KEYWORDS.get(rubric_key, []))
    if kw >= 4:
        return 3
    if kw >= 2:
        return 2
    if kw >= 1:
        return 1
    return 0


def _generate_feedback(
    rubric_scores: Dict[str, int],
    answers_count: int,
) -> str:
    """Build actionable textual feedback from rubric scores."""
    if answers_count == 0:
        return "No answers submitted yet. Complete the tasks and re-run scoring."

    perfect = all(v == 5 for v in rubric_scores.values())
    if perfect:
        return "Excellent work — full marks across every rubric category!"

    # Identify weak areas (score < 4) sorted ascending
    weak: List[Tuple[str, int]] = sorted(
        ((k, v) for k, v in rubric_scores.items() if v < 4),
        key=lambda kv: kv[1],
    )

    lines: List[str] = []
    if weak:
        top = weak[:3]
        lines.append("Areas to strengthen:")
        for key, score in top:
            label = RUBRIC_LABELS.get(key, key)
            if score == 0:
                lines.append(f"  • {label} ({score}/5) — not addressed; add a detailed answer.")
            elif score <= 2:
                lines.append(f"  • {label} ({score}/5) — consider expanding with specific details and keywords.")
            else:
                lines.append(f"  • {label} ({score}/5) — good start; add depth or concrete examples.")

    strong = [k for k, v in rubric_scores.items() if v >= 4]
    if strong:
        labels = [RUBRIC_LABELS.get(k, k) for k in strong]
        lines.append(f"Strong areas: {', '.join(labels)}.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_session(session: Session) -> Dict[str, Any]:
    """
    Score a session's submitted answers against the 8-category rubric.

    Returns a dict suitable for use as an event payload:
        problem, rubric_scores, overall_score, max_score,
        feedback, answers_count, per_task_scores
    """
    rubric_scores: Dict[str, int] = {key: 0 for key in RUBRIC_KEYWORDS}

    latest_answers = _collect_latest_answers(session)

    # --- Per-task scoring (6 tasks → 6 rubric categories) ----------------
    per_task_scores: Dict[str, int] = {}
    for task_id, rubric_key in TASK_TO_RUBRIC.items():
        answer = latest_answers.get(task_id, "")
        score = _score_answer(answer, rubric_key)
        rubric_scores[rubric_key] = score
        per_task_scores[task_id] = score

    # --- Cross-answer bonus for categories without a dedicated task ------
    combined_text = " ".join(latest_answers.values())
    for bonus_key in ("observability", "security"):
        rubric_scores[bonus_key] = max(
            rubric_scores[bonus_key],
            _cross_answer_bonus(combined_text, bonus_key),
        )

    overall = sum(rubric_scores.values())
    max_score = 5 * len(rubric_scores)

    feedback = _generate_feedback(rubric_scores, len(latest_answers))

    return {
        "problem": session.title,
        "rubric_scores": rubric_scores,
        "overall_score": overall,
        "max_score": max_score,
        "feedback": feedback,
        "answers_count": len(latest_answers),
        "per_task_scores": per_task_scores,
    }
