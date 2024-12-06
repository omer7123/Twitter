import uuid
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database.services.twit import twit_service_db
from api.users import router as user_router
from api.twit import router as twit_router

router = APIRouter()

active_connections: Dict[uuid.UUID, WebSocket] = {}


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: uuid.UUID):
    await websocket.accept()
    twit_service_db.connections[user_id] = websocket  # Сохраняем подключение
    try:
        while True:
            data = await websocket.receive_text()  # Поддержание соединения
    except WebSocketDisconnect:
        del twit_service_db.connections[user_id]  # Удаляем подключение при отключении


router.include_router(user_router)
router.include_router(twit_router)
