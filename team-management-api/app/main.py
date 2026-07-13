from fastapi import FastAPI

from app.api_routes.auth_routes import router as auth_router
from app.api_routes.users_routes import router as users_router
from app.api_routes.team_routes import router as teams_router
from app.api_routes.team_members_routes import router as team_member_router
from app.api_routes.task_routes import router as task_router
from app.api_routes.activity_routes import router as activity_router
from app.api_routes.sse_routes import router as sse_router
from app.api_routes.chat_router.websocket_routes import router as websocket_router
from app.api_routes.chat_router.chat_routes import router as chat_routes
from app.api_routes.chat_router.conversation_routes import router as conversation_routes
from app.api_routes.chat_router.direct_message_routes import router as direct_message_routes

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(teams_router)
app.include_router(team_member_router)
app.include_router(task_router)
app.include_router(activity_router)
app.include_router(sse_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")
app.include_router(chat_routes,prefix="/api")
app.include_router(conversation_routes,prefix="/api")
app.include_router(direct_message_routes, prefix="/api")