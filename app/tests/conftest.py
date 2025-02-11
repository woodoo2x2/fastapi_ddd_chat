from pytest import fixture

from infrastructure.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.dependency import init_mediator
from logic.mediator import Mediator


@fixture
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@fixture
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator