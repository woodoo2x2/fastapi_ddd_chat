from dataclasses import dataclass

from domain.entities.messages import Chat
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str



