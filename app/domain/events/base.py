import uuid
from abc import ABC
from dataclasses import dataclass, field


@dataclass
class BaseEvent(ABC):
    event_id : str = field(default_factory=uuid.uuid4, kw_only=True)
