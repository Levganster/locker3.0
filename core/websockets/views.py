
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status, Depends, Security

from core.websockets.connection_manager import ConnectionManager
from core.websockets.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

from core.websockets.dependencies import get_user_service

from core.auth.views import access_security


router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)
manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()  # Ожидание данных от клиента
            await manager.send_personal_message(f"Вы сказали: {data}", user_id)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        manager.disconnect(user_id)

# API для отправки сообщения от преподавателя всем клиентам
@router.post("/send_to_all")
async def send_to_all(
    message: str,
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    await manager.broadcast(message)
    return {"message": "Сообщение отправлено всем подключенным клиентам"}

@router.post("/send_personal_message")
async def send_personal_message(
    message: str,
    user_id: str,
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    await manager.send_personal_message(message, user_id)

@router.get("/get_active_connections")
def get_active_connections(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    return manager.get_active_connections()