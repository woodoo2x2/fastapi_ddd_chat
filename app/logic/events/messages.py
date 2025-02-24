from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.events.messages import NewChatCreatedEvent
from domain.values.message import Title
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.converters import convert_event_to_broker_message
from infrastructure.repositories.messages.base import (
    BaseChatRepository,
)
from logic.commands.base import CommandHandler
from logic.events.base import EventHandler
from logic.exceptions.messages import (
    ChatWithThatTitleAlreadyExistsException,
)


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> NewChatCreatedEvent:
        await self.message_broker.send_message(
            key=str(event.event_id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event)
        )

        print(f"Обработка события {event.title}")
