from datetime import datetime
from typing import Self

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.messages import Chat, Message


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return CreateChatResponseSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return CreateMessageResponseSchema(
            oid=message.oid, text=message.text.as_generic_type()
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> Self:
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at
        )


class ChatDetailResponseSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDetailResponseSchema":
        return ChatDetailResponseSchema(
            oid=chat.oid, title=chat.title.as_generic_type(), created_at=chat.created_at
        )


class GetMessagesResponseSchema(BaseQueryResponseSchema):
    items: list[MessageDetailSchema]
