from fastapi import FastAPI

from app.api_routes.auth_routes import router as auth_router
from app.api_routes.users_routes import router as users_router
from app.api_routes.team_routes import router as teams_router


app = FastAPI()


# Register auth routes
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(teams_router)