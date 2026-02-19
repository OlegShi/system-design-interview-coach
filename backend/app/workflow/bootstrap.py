from app.domain.models import Event, Session
from app.agents.planner_agent import run_planner_agent
from app.agents.specifier_agent import run_specifier_agent


def bootstrap_session(session: Session) -> Session:
    # system created
    session.events.append(Event(type="system", content="Session created"))

    # constitution
    session.events.append(Event(type="constitution_started", content="Defining interview principles"))
    session.events.append(
        Event(
            type="constitution_completed",
            content="Interview principles defined",
            payload={
                "principles": [
                    "Start with requirements and constraints (functional + non-functional).",
                    "State traffic assumptions (QPS, payload size, read/write ratio).",
                    "Design APIs and data model early.",
                    "Address scalability and bottlenecks (CPU, I/O, DB, network).",
                    "Discuss consistency tradeoffs and failure modes.",
                    "Include observability (metrics/logs/tracing) and SLOs.",
                    "Call out security and data privacy when relevant.",
                    "Be explicit about tradeoffs (cost vs latency vs correctness).",
                ],
                "rubric": {
                    "requirements": 0,
                    "api_design": 0,
                    "data_model": 0,
                    "scalability": 0,
                    "reliability": 0,
                    "observability": 0,
                    "security": 0,
                    "tradeoffs": 0,
                },
                "scoring_scale": {"min": 0, "max": 5, "meaning": "0=missing, 3=adequate, 5=excellent"},
            },
        )
    )

    # specify
    session.events.append(Event(type="specify_started", content="Defining problem statement and constraints"))
    session = run_specifier_agent(session)

    
     # plan
    session.events.append(Event(type="plan_started", content="Creating architecture plan outline"))
    session = run_planner_agent(session)


    return session
