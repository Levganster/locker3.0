import asyncio
import websockets

async def listen():
    uri = "ws://localhost:8000/websockets/ws"  # Адрес WebSocket-соединения
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()  # Ожидание сообщения от сервера
            print(f"Получено сообщение от сервера: {message}")

asyncio.run(listen())
