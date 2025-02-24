from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str

    title: ClassVar[str] = "New message received"


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str

    title: ClassVar[str] = "New chat created"
