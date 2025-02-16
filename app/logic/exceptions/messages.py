from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True,eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str
    @property
    def message(self) -> str:
        return f"Chat with title {self.title} already exists."


@dataclass(frozen=True, eq=False)
class ChatWithThatOidNotFoundException(LogicException):
    chat_oid: str
    @property
    def message(self) -> str:
        return f"Chat with oid {self.chat_oid} not found."