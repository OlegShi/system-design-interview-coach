from app.domain.models import Event, Session
from app.skills.task_skill import generate_interview_tasks


def run_task_generator_agent(session: Session) -> Session:
    """
    Generates interview tasks/questions to drive the session.
    Later: LLM-driven task sequencing and adaptive difficulty.
    """
    session.events.append(
        Event(
            type="task_generator_agent_started",
            content="Task generator agent running",
        )
    )

    payload = generate_interview_tasks(session.title)

    session.events.append(
        Event(
            type="task_generator_agent_completed",
            content="Task generator agent produced interview tasks",
            payload=payload,
        )
    )

    return session
