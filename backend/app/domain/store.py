from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID

from .models import Session


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: Dict[UUID, Session] = {}

    def create(self, session: Session) -> Session:
        self._sessions[session.id] = session
        return session

    def get(self, session_id: UUID) -> Optional[Session]:
        return self._sessions.get(session_id)

    def list(self) -> list[Session]:
        # simple ordering by created_at (newest last)
        return sorted(self._sessions.values(), key=lambda s: s.created_at)
