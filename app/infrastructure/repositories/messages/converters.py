from typing import Mapping, Any

from domain.entities.messages import Chat, Message
from domain.values.message import Title, Text


def convert_message_entity_to_document(message: Message) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
    }


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        text=Text(message_document["text"]),
        oid=message_document["oid"],
    )


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [
            convert_message_entity_to_document(message) for message in chat.messages
        ],
    }


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        title=Title(chat_document.get("title")),
        created_at=chat_document.get("created_at"),
        oid=chat_document.get("oid"),
        messages=[
            convert_message_document_to_entity(document)
            for document in chat_document.get("messages")
        ],
    )
