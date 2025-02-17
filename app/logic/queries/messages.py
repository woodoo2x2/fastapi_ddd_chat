from dataclasses import dataclass
from typing import Generic

from domain.entities.messages import Chat
from infrastructure.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from logic.exceptions.messages import ChatWithThatOidNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler, QT, QR


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QT, QR]):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)
        if not chat:
            raise ChatWithThatOidNotFoundException(chat_oid=query.chat_oid)
        return chat
