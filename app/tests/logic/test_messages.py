import pytest

from infrastructure.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator
from tests.conftest import chat_repository, mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
        mediator: Mediator,
        chat_repository: BaseChatRepository,
):
    print(f"Handlers for CreateChatCommand: {mediator.command_map.get(CreateChatCommand)}")
    chat = (await mediator.handle_command(CreateChatCommand(title='test title')))[0]

    assert (await chat_repository.check_chat_exists_by_title(title=chat.title))
