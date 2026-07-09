from fastapi import FastAPI

from app.api_routes.auth_routes import router as auth_router
from app.api_routes.users_routes import router as users_router
from app.api_routes.team_routes import router as teams_router
from app.api_routes.team_members_routes import router as team_member_router
from app.api_routes.task_routes import router as task_router
from app.api_routes.activity_routes import router as activity_router
from app.api_routes.sse_routes import router as see_router

app = FastAPI()


# Register auth routes
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(teams_router)
app.include_router(team_member_router)
app.include_router(task_router)
app.include_router(activity_router)
app.include_router(see_router,prefix="/api")