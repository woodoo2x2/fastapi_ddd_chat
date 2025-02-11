from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True,eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str
    @property
    def message(self) -> str:
        return f"Chat with title {self.title} already exists."