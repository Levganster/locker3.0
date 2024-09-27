from fastapi import FastAPI, WebSocket

from core.log.logger import log_connection, log_authorization, log_disconnection

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}  # Используем словарь для хранения идентификаторов
        self.active_users: dict[str,str,str,str, str, str] = []

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket  # Сохраняем WebSocket под уникальным user_id
        self.active_users.append({"id": user_id, "name": None, "group": None})
        log_connection(user_id)

    async def delete_active_user(self, user_id: str):
        for user in self.active_users:
            if user['id'] == user_id:
                log_disconnection(user_id, user['name'], user['group'])
                self.active_users.remove(user)

    async def disconnect(self, user_id: str):
        websocket = self.active_connections.pop(user_id, None)
        if websocket:
            await websocket.close()
            for user in self.active_users:
                if user['id'] == user_id:
                    log_disconnection(user_id, user['name'], user['group'])
                    self.active_users.remove(user)

    async def send_personal_message(self, message: str, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        try:
            for _, connection in self.active_connections.items():
                await connection.send_text(message)
        except Exception as e:
            print(e)


    def get_active_connections(self):
        return sorted(self.active_users, key=lambda x: x['id'])
    
    async def add_active_user(self, user_id, name, group):
        for user in self.active_users:
            if user['id'] == user_id:
                user['name'] = name  # Обновление имени пользователя
                user['group'] = group
                break
        log_authorization(user_id, name, group)