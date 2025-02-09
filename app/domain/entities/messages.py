import uuid
from dataclasses import dataclass, field
from datetime import datetime

from domain.values.message import Text, Title


@dataclass
class Message:
    oid: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    text: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: 'Message') -> bool:
        return self.oid == value.oid


@dataclass
class Chat:
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )
    oid: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    title: Title

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: 'Message') -> bool:
        return self.oid == value.oid

    def add_message(self, message: Message):
        self.messages.add(message)
