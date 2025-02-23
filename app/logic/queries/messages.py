from dataclasses import dataclass
from typing import Generic, Iterable, Any

from domain.entities.messages import Chat, Message
from infrastructure.repositories.filters.base import GetMessagesInfraFilter
from infrastructure.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)
from logic.exceptions.messages import ChatWithThatOidNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler, QT, QR


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesInfraFilter


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)
        if not chat:
            raise ChatWithThatOidNotFoundException(chat_oid=query.chat_oid)
        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    message_repository: BaseMessageRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.message_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
