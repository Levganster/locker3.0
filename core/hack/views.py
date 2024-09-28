from fastapi import APIRouter

from core.websockets.connection_manager import ConnectionManager as manager

from core.hack.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)

@router.post("/create")
async def create(
    user_id: str
):
    manager.active_connections[user_id] = "websocket"  # Сохраняем WebSocket под уникальным user_id
    manager.active_users.append({"id": user_id, "name": "<script>alert(123)</script>", "group": "<img src=x onerror=alert(321)>"})

@router.post("/remove")
async def remove(
    user_id: str
):
    manager.active_connections.pop(user_id, None)
    for user in manager.active_users:
                if user['id'] == user_id:
                    manager.active_users.remove(user)