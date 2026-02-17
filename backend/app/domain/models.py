from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str
    content: str


class Session(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: str
    events: List[Event] = Field(default_factory=list)
