from fastapi import APIRouter, HTTPException, Depends
from punq import Container
from starlette import status


from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
from logic.dependency import init_container
from logic.mediator import Mediator

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post('/',
             response_model=CreateChatResponseSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create chat message',

             )
async def create_chat_handler(data: CreateChatRequestSchema,
                              container: Container  = Depends(init_container),):
    """Create chat message"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=data.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)
