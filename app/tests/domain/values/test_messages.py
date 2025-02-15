from datetime import datetime

import pytest

from domain.entities.messages import Message, Chat
from domain.events.messages import NewMessageReceivedEvent
from domain.exceptions.messages import TitleTooLongException
from domain.values.message import Text, Title


def test_create_short_message_success():
    text = Text('Test success')
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_long_message_success():
    text = Text('a' * 400)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title('Test title')
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title('Test title' * 100)


def test_add_message_to_chat():
    text = Text('a' * 400)
    message = Message(text=text)

    title = Title('Test title')
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_new_message_events():
    text = Text('Test text')
    message = Message(text=text)

    title = Title('Test title')
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events
    assert len(events) == 1

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
