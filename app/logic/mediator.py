from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.events.base import BaseEvent
from logic.commands.base import CommandHandler, CT, CR, BaseCommand
from logic.events.base import EventHandler, ET, ER
from logic.exceptions.mediator import EventHandlerNotRegisteredException, CommandHandlerNotRegisteredException


@dataclass(eq=False)
class Mediator:
    event_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    command_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    def register_event(self, event: ET, event_handler: [EventHandler[ET, ER]]):
        self.event_map[event].append(event_handler)

    def register_command(self, command: CT, command_handler: [EventHandler[CT, CR]]):
        self.command_map[command].extend(command_handler)

    async def handle_event(self, event: BaseEvent) -> list[ER]:
        event_type = event.__class__
        handlers = self.event_map.get(event.__class__)

        if not handlers:
            raise EventHandlerNotRegisteredException(event_type)

        return [await handler.handle(event) for handler in handlers]

    async def handle_command(self, command: BaseCommand) -> list[CR]:
        event_type = command.__class__
        handlers = self.command_map.get(command.__class__)

        if not handlers:
            raise CommandHandlerNotRegisteredException(event_type)

        result = [await handler.handle(command) for handler in handlers]

        return result
