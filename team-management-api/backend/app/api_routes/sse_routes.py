import json
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.sse_manager import sse_manager


router  = APIRouter(
    prefix="/events",
    tags=["SSE"]
)


async def event_generator(team_id : UUID):

    # Streams events to a connected client.

    queue = await sse_manager.connect(team_id)

    try:
        while True:

            event = await queue.get()

            yield (
                f"data : {json.dumps(event)}\n\n"
            )

    finally:
        sse_manager.disconnect(team_id,queue)


@router.get("/teams/{team_id}")
async def stream_event(
    team_id: UUID
):

    return StreamingResponse(
        event_generator(team_id),
        media_type="text/event-stream"
    )