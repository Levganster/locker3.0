import re
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Security

from core.websockets.connection_manager import ConnectionManager
from core.websockets.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

from fastapi_jwt import JwtAuthorizationCredentials

from core.auth.views import access_security, admin_required


router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)
manager = ConnectionManager()

def validate_format(s):
    pattern = r"username: (\w+), group: (\w+)"
    return bool(re.match(pattern, s))

def extract_values(s):
    # Регулярное выражение с группами захвата для username и group
    pattern = r'username: (\w+), group: (\w+)'
    match = re.match(pattern, s)
    if match:
        username = match.group(1)
        group = match.group(2)
        if group == "None":
            group = None
        return username, group
    return None, None

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()  # Ожидание данных от клиента
            await manager.send_personal_message(f"Вы сказали: {data}", user_id)
            if validate_format(data):
                username, group = extract_values(data)
                await manager.add_active_user(user_id, username, group)
    except WebSocketDisconnect:
        print(f"Пользователь {user_id} отключился")
        await manager.delete_active_user(user_id)
    except Exception as e:
        print(f"Connection error: {e}")

# API для отправки сообщения от преподавателя всем клиентам
@router.post("/send_to_all")
async def send_to_all(
    message: str,
    credentials: JwtAuthorizationCredentials = Depends(admin_required),
):
    await manager.broadcast(message)
    return {"message": "Сообщение отправлено всем подключенным клиентам"}

@router.post("/send_personal_message")
async def send_personal_message(
    message: str,
    user_id: str,
    credentials: JwtAuthorizationCredentials = Depends(admin_required),
):
    await manager.send_personal_message(message, user_id)

@router.get("/get_active_connections")
def get_active_connections(
    credentials: JwtAuthorizationCredentials = Depends(admin_required),
):
    return manager.get_active_connections()