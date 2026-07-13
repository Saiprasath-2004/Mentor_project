from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.database import SessionLocal
from app.core.websocket_manager import websocket_manager

from app.dependencies.websocket_dependencies import (
    get_current_websocket_user
)
from app.schemas.chat_schemas import ChatMessageCreate
from app.schemas.direct_message_schemas import DirectMessageCreate

from app.services.chat_service import ChatService
from app.services.direct_message_service import DirectMessageService
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"]
)

chat_service = ChatService()
direct_message_service =  DirectMessageService()
conversation_service = ConversationService()

@router.websocket("/teams/{team_id}")
async def websocket_chat(
    websocket: WebSocket,
    team_id: UUID,
):

    async with SessionLocal() as db:

        try:

            current_user = await get_current_websocket_user(
                websocket,
                db
            )

            await websocket_manager.connect(
                team_id,
                websocket
            )

            await websocket_manager.send_personal_message(
                websocket,
                {
                    "type": "connected",
                    "message": "Connected successfully."
                }
            )

            while True:

                data = await websocket.receive_json()

                chat = await chat_service.create_message(
                    db=db,
                    team_id=team_id,
                    message_data=ChatMessageCreate(
                        message=data["message"]
                    ),
                    current_user=current_user
                )

                await websocket_manager.broadcast(
                    team_id,
                    chat.model_dump(mode="json")
                )

        except WebSocketDisconnect:

            websocket_manager.disconnect(
                team_id,
                websocket
            )

        except Exception as exc:

            await websocket_manager.send_personal_message(
                websocket,
                {
                    "type": "error",
                    "message": str(exc)
                }
            )

            websocket_manager.disconnect(
                team_id,
                websocket
            )

@router.websocket("/conversations/{conversation_id}")
async def websocket_direct_chat(
    websocket:WebSocket,
    conversation_id: UUID
):
    async with SessionLocal() as db:

        try:

            # Authenticate user
            current_user = await get_current_websocket_user(
                websocket,
                db
            )

            #verify user belongs to this conversation
            await conversation_service.get_conversation(
                db=db,
                conversation_id=conversation_id,
                current_user=current_user
            )

            # Register websocket
            await websocket_manager.connect(
                conversation_id,
                websocket
            )

            # Notify successful connection
            await websocket_manager.send_personal_message(
                websocket,
                {
                    "type": "connected",
                    "message": "Connected successfully."
                }
            )


            while True:

                data = await websocket.receive_json()

                message = await direct_message_service.send_message(
                    db = db,
                    conversation_id=conversation_id,
                    message_data= DirectMessageCreate(
                        message = data["message"]
                    ),
                    current_user=current_user
                )

                await websocket_manager.broadcast(
                    conversation_id,
                    message.model_dump(mode="json")
                )
            
        except WebSocketDisconnect:

            websocket_manager.disconnect(
                conversation_id,
                websocket
            )

        except Exception as exc:

            await websocket_manager.send_personal_message(
                websocket,
                {
                    "type" : "error",
                    "message": str(exc)
                }
            )

            websocket_manager.disconnect(
                conversation_id,
                websocket
            )