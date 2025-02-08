from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True,eq=False)
class TextTooLongException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Too long message: {self.text[:255]}..."