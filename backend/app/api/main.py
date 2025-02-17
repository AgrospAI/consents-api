from app.api.routes import consents, login, utils
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(consents.router)
api_router.include_router(utils.router)
