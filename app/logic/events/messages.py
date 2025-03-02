from dataclasses import dataclass

from domain.events.messages import NewChatCreatedEvent, NewMessageReceivedEvent
from infrastructure.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import EventHandler


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            key=str(event.event_id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )

        print(f"Обработка события {event.title}")


@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            key=str(event.event_id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )

        print(f"Обработка события {event.title}")
