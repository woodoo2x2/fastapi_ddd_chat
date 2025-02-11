from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.messages import Chat


@dataclass
class BaseChatRepository(ABC):
    title: str

    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...

@dataclass
class MemoryChatRepository(ABC):
    __saved_chats: list[Chat] = field(
        default_factory=list,
        kw_only=True,
    )

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(chat for chat in self.__saved_chats if chat.title == title))
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self.__saved_chats.append(chat)