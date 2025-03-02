import json

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

router = APIRouter(tags=["chats"], prefix="/ws")

# POSTMAN: ws://localhost:8000/ws/92f31e89-bf10-499f-b2f3-0ab4dd2d3a8f

@router.websocket("/{chat_oid}/")
async def message_handlers(chat_oid:str, websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        await websocket.send_text(json.dumps(data))
