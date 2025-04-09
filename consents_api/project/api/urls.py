from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consents.router import router as consents_router
from users.router import router as users_router
from assets.router import router as assets_router

router = DefaultRouter()

router.registry.extend(assets_router.registry)
router.registry.extend(consents_router.registry)
router.registry.extend(users_router.registry)


urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include("docs.urls")),
]
