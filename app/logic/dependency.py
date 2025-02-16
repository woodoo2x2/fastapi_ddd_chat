from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from infrastructure.repositories.messages.base import BaseChatRepository
from infrastructure.repositories.messages.mongo import MongoDBChatRepository, MongoDBMessageRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler, CreateMessageCommand, \
    CreateMessageCommandHandler
from logic.mediator import Mediator
from settings.config import Settings


@lru_cache(maxsize=1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)


    def create_mongo_db_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGO_DB_PATH,
                                  serverSelectionTimeoutMS=3000)

    container.register(AsyncIOMotorClient, factory=create_mongo_db_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongo_db_repository() -> MongoDBChatRepository:
        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_DB_DATABASE_NAME,
            mongo_db_collection_name=settings.MONGO_DB_CHAT_COLLECTION_NAME,

        )

    def init_message_mongo_db_repository() -> MongoDBMessageRepository:
        return MongoDBMessageRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.MONGO_DB_DATABASE_NAME,
            mongo_db_collection_name=settings.MONGO_DB_CHAT_COLLECTION_NAME,

        )

    container.register(BaseChatRepository, factory=init_chat_mongo_db_repository, scope=Scope.singleton)
    container.register(MongoDBMessageRepository, factory=init_message_mongo_db_repository, scope=Scope.singleton)

    container.register(CreateMessageCommandHandler)
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
