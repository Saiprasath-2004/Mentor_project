from uuid import UUID

from fastapi import WebSocket


class WebSocketManager:
    """
    Manages active WebSocket connections for each team.
    Every team acts as its own chat room.
    """

    def __init__(self):
        self.rooms: dict[UUID, list[WebSocket]] = {}

    async def connect(
        self,
        team_id: UUID,
        websocket: WebSocket
    ):
        await websocket.accept()

        if team_id not in self.rooms:
            self.rooms[team_id] = []

        self.rooms[team_id].append(websocket)

        # Optional welcome message
        await websocket.send_text("Connected!")

    def disconnect(
        self,
        team_id: UUID,
        websocket: WebSocket
    ):

        if team_id not in self.rooms:
            return

        if websocket in self.rooms[team_id]:
            self.rooms[team_id].remove(websocket)

        if not self.rooms[team_id]:
            del self.rooms[team_id]

    async def broadcast(
        self,
        team_id: UUID,
        message: dict
    ):

        if team_id not in self.rooms:
            return

        for websocket in self.rooms[team_id]:
            await websocket.send_json(message)

    async def send_personal_message(
        self,
        websocket: WebSocket,
        message: dict
    ): 
        # Send a message to only one connected client.

        await websocket.send_json(message)


websocket_manager = WebSocketManager()