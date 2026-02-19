from app.domain.models import Event, Session
from app.skills.scoring_skill import generate_initial_score


def run_scorer_agent(session: Session) -> Session:
    """
    Stub Scorer Agent.
    Later: score candidate answers against rubric using LLM + eval harness.
    """
    session.events.append(Event(type="scorer_agent_started", content="Scorer agent running"))

    payload = generate_initial_score(session.title)

    session.events.append(
        Event(
            type="scorer_agent_completed",
            content="Scorer agent produced rubric score",
            payload=payload,
        )
    )

    return session
