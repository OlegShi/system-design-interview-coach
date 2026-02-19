from app.agents.scorer_agent import run_scorer_agent
from app.agents.task_generator_agent import run_task_generator_agent
from app.domain.models import Event, Session


def has_event(session: Session, event_type: str) -> bool:
    return any(e.type == event_type for e in session.events)


def run_next_steps(session: Session) -> Session:
    """
    Minimal deterministic step runner.
    Later this becomes a LangGraph state machine / agent loop.
    """

    # If tasks not present, generate tasks
    if not has_event(session, "task_generator_agent_completed"):
        session.events.append(Event(type="tasks_started", content="Generating interview tasks (on-demand)"))
        return run_task_generator_agent(session)

    # If scoring not present, score
    if not has_event(session, "scorer_agent_completed"):
        session.events.append(Event(type="scoring_started", content="Scoring session state (on-demand)"))
        return run_scorer_agent(session)

    # Nothing to do
    session.events.append(Event(type="run_noop", content="No pending steps to run"))
    return session
