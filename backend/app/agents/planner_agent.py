from app.domain.models import Event, Session
from app.skills.plan_skill import generate_plan_outline


def run_planner_agent(session: Session) -> Session:
    """
    Stub Planner Agent.
    Today: deterministic skill call.
    Later: LLM-driven reasoning + MCP tool calls.
    """
    session.events.append(Event(type="planner_agent_started", content="Planner agent running"))

    plan_payload = generate_plan_outline(session.title)

    session.events.append(
        Event(
            type="planner_agent_completed",
            content="Planner agent produced plan outline",
            payload=plan_payload,
        )
    )

    return session
