from app.domain.models import Event, Session
from app.skills.scoring_skill import score_session


def run_scorer_agent(session: Session) -> Session:
    """
    Scorer Agent — evaluates candidate answers against the 8-category rubric.

    Delegates all scoring logic to scoring_skill.score_session().
    Later: swap heuristic scoring for LLM + eval harness.
    """
    session.events.append(
        Event(type="scorer_agent_started", content="Scorer agent evaluating submitted answers")
    )

    payload = score_session(session)

    overall = payload["overall_score"]
    max_score = payload["max_score"]
    answered = payload["answers_count"]
    content = (
        f"Scoring complete — {overall}/{max_score} overall "
        f"({answered} answer(s) evaluated)"
    )

    session.events.append(
        Event(
            type="scorer_agent_completed",
            content=content,
            payload=payload,
        )
    )

    return session
