from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic


@dataclass(frozen=True)
class BaseCommand(ABC):
    """
    Базовый класс для команд в паттерне CQRS.

    Команда — это объект, который описывает намерение изменить состояние системы.
    Этот класс является абстрактным и должен быть унаследован конкретными командами.

    Атрибуты:
        (нет, но дочерние классы должны определять свои атрибуты)
    """

    ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR", bound=Any)


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    """
    Базовый класс обработчика команд в паттерне CQRS.

    Обработчик команд отвечает за выполнение команд и изменение состояния системы.
    Это абстрактный класс, который должен быть унаследован и реализован.

    Параметры типа (Generics):
        CT (Command Type) — тип команды, наследник BaseCommand.
        CR (Command Response) — тип результата выполнения команды.

    Методы:
        handle(command: CT) -> CR:
            Абстрактный метод, который должен быть реализован в дочерних классах.
            Он принимает команду типа CT и возвращает результат типа CR.
    """

    @abstractmethod
    def handle(self, command: CT) -> CR: ...
