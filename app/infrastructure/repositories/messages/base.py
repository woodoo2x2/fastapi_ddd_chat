from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import Chat, Message
from infrastructure.repositories.filters.base import GetMessagesInfraFilter


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat: ...

    @abstractmethod
    async def add_chat(self, chat_oid: Chat) -> None: ...


@dataclass
class BaseMessageRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> Message: ...

    @abstractmethod
    async def get_messages(
        self, chat_oid: str, filters: GetMessagesInfraFilter
    ) -> tuple[Iterable[Message], int]: ...
