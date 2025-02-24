from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Type

from domain.events.base import BaseEvent
from logic.commands.base import CommandHandler, CT, CR, BaseCommand
from logic.events.base import EventHandler, ET, ER
from logic.exceptions.mediator import (
    CommandHandlerNotRegisteredException,
)
from logic.mediator.command import CommandMediator

from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import BaseQuery, BaseQueryHandler, QT, QR


@dataclass(eq=False)
class Mediator(EventMediator, QueryMediator, CommandMediator):
    event_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    command_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    query_map: dict[QT, BaseQueryHandler] = field(
        default_factory=lambda: {}, kw_only=True
    )

    def register_event(self, event: ET, event_handler: [EventHandler[ET, ER]]):
        self.event_map[event].extend(event_handler)

    def register_command(
        self, command: Type[CT], command_handler: [CommandHandler[CT, CR]]
    ):
        self.command_map[command].extend(command_handler)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        self.query_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.event_map[event.__class__]

            for handler in handlers:
                result.append(await handler.handle(event=event))

            result.extend([await handler.handle(event) for handler in handlers])


        return result

    async def handle_command(self, command: BaseCommand) -> list[CR]:
        event_type = command.__class__
        handlers = self.command_map.get(command.__class__)

        if not handlers:
            raise CommandHandlerNotRegisteredException(event_type)

        result = [await handler.handle(command) for handler in handlers]

        return result

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.query_map[query.__class__].handle(query=query)
