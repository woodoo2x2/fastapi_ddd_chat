import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass
class BaseEvent(ABC):
    title: ClassVar[str]
    event_id: str = field(default_factory=uuid.uuid4, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
