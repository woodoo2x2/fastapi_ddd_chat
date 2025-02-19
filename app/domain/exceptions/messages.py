from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Too long message: {self.text[:255]}..."


@dataclass(frozen=True, eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self) -> str:
        return "You send an empty message"
