from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from starlette.config import Config

from infrastructure.repositories.messages.base import BaseChatRepository
from infrastructure.repositories.messages.mongo import MongoDBChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from settings.config import Settings


@lru_cache(maxsize=1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateChatCommandHandler)
    container.register(Settings, instance=Settings() ,scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    def init_chat_mongo_db_repository() -> MongoDBChatRepository:
        settings: Settings = container.resolve(Settings)
        client = AsyncIOMotorClient(settings.MONGO_DB_PATH,
                                    serverSelectionTimeoutMS=3000)

        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_DB_DATABASE_NAME,
            mongo_db_collection_name=settings.MONGO_DB_CHAT_COLLECTION_NAME,

        )
    container.register(BaseChatRepository, factory=init_chat_mongo_db_repository, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator)

    return container
