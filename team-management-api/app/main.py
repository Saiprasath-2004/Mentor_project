from fastapi import FastAPI

from app.api_routes.auth_routes import router as auth_router


app = FastAPI()


# Register auth routes
app.include_router(auth_router)