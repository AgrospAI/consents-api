from fastapi.routing import APIRouter

from consents_api.web.api import consent, docs, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(docs.router)
api_router.include_router(consent.router)
