from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.domain.models import Event, Session
from app.domain.store import InMemorySessionStore
from app.workflow.bootstrap import bootstrap_session


router = APIRouter(prefix="/sessions", tags=["sessions"])

store = InMemorySessionStore()


class CreateSessionRequest(BaseModel):
    title: str


@router.post("", response_model=Session)
def create_session(req: CreateSessionRequest) -> Session:
    session = Session(title=req.title)
    session = bootstrap_session(session)
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

@router.post("/{session_id}/run", response_model=Session)
def run_session(session_id: UUID) -> Session:
    session = store.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # For now: just append a marker event to prove we can "run" later steps
    session.events.append(Event(type="run_requested", content="Run requested by user"))

    # Later: this will call a state machine / next-step runner
    # session = run_next_steps(session)

    store.create(session)  # overwrite in store
    return session

