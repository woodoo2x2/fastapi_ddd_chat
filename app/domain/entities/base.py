import uuid
from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime

from domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    oid: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        kw_only=True,
    )
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def pull_events(self) -> list[BaseEvent]:
        register_events = copy(self._events)
        self._events.clear()
        return register_events

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)
