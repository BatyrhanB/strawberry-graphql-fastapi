import uvicorn
import uuid

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

from src.settings.config import settings
from src.auth.schemas import UserRead, UserCreate
from src.auth.models import User
from src.auth.managers import get_user_manager
from src.auth.security import auth_backend


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)