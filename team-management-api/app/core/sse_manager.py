import asyncio
from uuid import UUID

class SSEManager:

    """
        Manages all active Server-Sent Event connections.

        Keeps track of connected SSE clients per team.

        Each team has its own list of client queues.
        Events are broadcast only to clients connected
        to that specific team..
    """

    def __init__(self):
        
        #Store one queue per connected client
        self.clients: dict[UUID,list[asyncio.Queue]] = {}

    async def connect(self, team_id: UUID) -> asyncio.Queue:
         
         #Register a new client and return its event queue

         queue = asyncio.Queue()

         if team_id not in self.clients:
             self.clients[team_id] =[]
         self.clients[team_id].append(queue)
         return queue
    
    def disconnect(self, team_id: UUID, queue: asyncio.Queue):

        if team_id not in self.clients:
            return
        #Remove a disconnceted client's queue

        if queue in self.clients[team_id]:
            self.clients[team_id].remove(queue)

        # Remove empty room
        if not self.clients[team_id]:
            del self.clients[team_id]

    async def broadcast(self,team_id: UUID, event: dict):
        

        if team_id not in self.clients:
            return
        #send an event  to every connected client
        for queue in self.clients[team_id]:
            await queue.put(event)


# Single shared manager used across the applicatipn
sse_manager = SSEManager()