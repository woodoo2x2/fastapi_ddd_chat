from fastapi import APIRouter, HTTPException, Depends
from punq import Container
from starlette import status

from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema, \
    CreateMessageRequestSchema, CreateMessageResponseSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand, CreateMessageCommandHandler
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
             responses={
                 status.HTTP_200_OK: {'model': CreateChatResponseSchema},
                 status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
             })
async def create_chat_handler(data: CreateChatRequestSchema,
                              container: Container = Depends(init_container), ) -> CreateChatResponseSchema:
    """Create chat message"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=data.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post('/{chat_oid}/message',
             status_code=status.HTTP_201_CREATED,
             description='Create chat message',
             responses={
                 status.HTTP_200_OK: {'model': CreateChatResponseSchema},
                 status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
             })
async def create_message_handler(
        chat_oid: str,
        data: CreateMessageRequestSchema,
        container: Container = Depends(init_container), ):
    """Create chat message"""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=data.text, chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateMessageResponseSchema.from_entity(message)
