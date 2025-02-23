from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.events.base import BaseEvent
from logic.events.base import EventHandler, ET, ER


@dataclass(eq=False)
class EventMediator(ABC):
    event_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    def register_event(self, event: ET, event_handler: [EventHandler[ET, ER]]): ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]: ...
