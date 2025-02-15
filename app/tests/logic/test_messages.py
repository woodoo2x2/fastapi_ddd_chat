import pytest
from faker import Faker

from domain.entities.messages import Chat
from domain.values.message import Title
from infrastructure.repositories.messages.base import BaseChatRepository

from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from logic.mediator import Mediator



@pytest.mark.asyncio
async def test_create_chat_command_success(
        mediator: Mediator,
        chat_repository: BaseChatRepository,
        faker: Faker,
):

    chat, *_ = await mediator.handle_command(CreateChatCommand(title=faker.text()))

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())

@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
        mediator: Mediator,
        chat_repository: BaseChatRepository,
        faker: Faker,
):
    title = faker.text()
    chat = Chat(title=Title(title))

    await chat_repository.add_chat(chat)

    assert chat in chat_repository._saved_chats

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title))

    assert len(chat_repository._saved_chats) == 1