from punq import Container
from pytest import fixture

from infrastructure.repositories.messages.base import BaseChatRepository
from logic.mediator.base import Mediator
from tests.fixture import init_dummy_container


@fixture
def container() -> Container:
    return init_dummy_container()


@fixture
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)
