from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.domain.models import Event, Session
from app.domain.store import InMemorySessionStore

router = APIRouter(prefix="/sessions", tags=["sessions"])

store = InMemorySessionStore()


class CreateSessionRequest(BaseModel):
    title: str


@router.post("", response_model=Session)
def create_session(req: CreateSessionRequest) -> Session:
    session = Session(title=req.title)

    # Event 1 — system created session
    session.events.append(
        Event(type="system", content="Session created")
    )

    # Event 2 — constitution phase started
    session.events.append(
        Event(type="constitution_started", content="Defining interview principles")
    )

    # Event 3 — constitution phase completed (stubbed)
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
                "scoring_scale": {
                    "min": 0,
                    "max": 5,
                    "meaning": "0=missing, 3=adequate, 5=excellent",
                },
            },
        )
    )
    
        # Event 4 — specify phase started
    session.events.append(
        Event(
            type="specify_started",
            content="Defining problem statement and constraints",
        )
    )

    # Event 5 — specify phase completed (stubbed)
    session.events.append(
        Event(
            type="specify_completed",
            content="Problem specification defined",
            payload={
                "problem_statement": session.title,
                "assumptions": {
                    "qps": 1000,
                    "read_write_ratio": "80/20",
                    "average_payload_kb": 2,
                    "availability_target": "99.9%",
                    "region": "multi-region",
                },
                "non_functional_requirements": [
                    "Low latency (<100ms p95)",
                    "Horizontal scalability",
                    "Graceful degradation under load",
                ],
                "constraints": [
                    "Use commodity cloud infrastructure",
                    "Assume eventual consistency is acceptable",
                ],
            },
        )
    )



    return store.create(session)



@router.get("", response_model=list[Session])
def list_sessions() -> list[Session]:
    return store.list()


@router.get("/{session_id}", response_model=Session)
def get_session(session_id: UUID) -> Session:
    session = store.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
