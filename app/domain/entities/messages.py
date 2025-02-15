from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageReceivedEvent, NewChatCreatedEvent
from domain.values.message import Text, Title


@dataclass
class Message(BaseEntity):
    text: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: 'Message') -> bool:
        return self.oid == value.oid


@dataclass
class Chat(BaseEntity):
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    title: Title

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreatedEvent(chat_oid=new_chat.oid, chat_title=new_chat.title.as_generic_type()))
        return new_chat

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: 'Message') -> bool:
        return self.oid == value.oid

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(),
            message_oid=message.oid,
            chat_oid=self.oid,
        ))
