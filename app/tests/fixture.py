from punq import Container, Scope

from infrastructure.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.dependency import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    return container

