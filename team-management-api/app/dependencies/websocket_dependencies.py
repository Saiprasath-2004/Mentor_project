from uuid import UUID

from fastapi import WebSocket, WebSocketException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.repository.user_repository import UserRepository

user_repo = UserRepository()


async def get_current_websocket_user(
    websocket: WebSocket,
    db: AsyncSession,
):
    """
    Authenticate websocket connection using the JWT
    passed as:

    ws://.../ws/teams/{team_id}?token=JWT
    """

    token = websocket.query_params.get("token")

    if token is None:

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Authentication token missing."
        )

    try:

        payload = decode_token(token)

        user_id = UUID(payload["sub"])

    except (JWTError, KeyError, ValueError):

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid token."
        )

    user = await user_repo.get_by_id(
        db,
        user_id
    )

    if user is None:

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="User not found."
        )

    return user