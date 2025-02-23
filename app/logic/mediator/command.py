from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type

from logic.commands.base import CommandHandler, CT, CR, BaseCommand


@dataclass(eq=False)
class CommandMediator(ABC):
    command_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    def register_command(
        self, command: Type[CT], command_handler: [CommandHandler[CT, CR]]
    ): ...

    @abstractmethod
    async def handle_command(self, command: BaseCommand) -> list[CR]: ...
