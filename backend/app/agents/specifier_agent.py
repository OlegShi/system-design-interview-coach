from app.domain.models import Event, Session
from app.skills.assumptions_skill import generate_default_assumptions
from app.agents.agent_loader import load_instructions


def run_specifier_agent(session: Session) -> Session:
    """
    Stub Specifier Agent.
    Today: deterministic assumptions + canned requirements.
    Later: LLM reasoning + MCP question bank + user-specific constraints.
    """
    instructions = load_instructions("specifier/instructions.md")
    session.events.append(
        Event(
            type="specifier_agent_started",
            content="Specifier agent running",
            payload={"instructions_md": instructions},
        )
    )

    assumptions = generate_default_assumptions(session.title)

    payload = {
        "problem_statement": session.title,
        "assumptions": assumptions,
        "non_functional_requirements": [
            "Low latency (p95 target defined per system)",
            "Horizontal scalability",
            "Graceful degradation under load",
        ],
        "constraints": [
            "Use commodity cloud infrastructure",
            "Prefer simpler components unless requirements force complexity",
        ],
    }

    session.events.append(
        Event(
            type="specifier_agent_completed",
            content="Specifier agent produced problem specification",
            payload=payload,
        )
    )

    return session
