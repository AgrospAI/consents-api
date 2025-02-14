from fastapi import APIRouter

from app.api.routes import login, consents

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(consents.router)
