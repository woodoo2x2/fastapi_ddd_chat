from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope


from infrastructure.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)
from infrastructure.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessageRepository,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from settings.config import Settings


@lru_cache(maxsize=1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)

    def create_mongo_db_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGO_DB_PATH, serverSelectionTimeoutMS=3000)

    container.register(
        AsyncIOMotorClient, factory=create_mongo_db_client, scope=Scope.singleton
    )
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
            mongo_db_collection_name=settings.MONGO_DB_MESSAGES_COLLECTION_NAME,
        )

    # Repository Registration
    container.register(
        BaseChatRepository, factory=init_chat_mongo_db_repository, scope=Scope.singleton
    )
    container.register(
        BaseMessageRepository,
        factory=init_message_mongo_db_repository,
        scope=Scope.singleton,
    )
    # Command Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query Handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_handler =  CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )

        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
            message_repository=container.resolve(BaseMessageRepository),
        )
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)
    return container
