from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assets.router import router as assets_router
from users.router import router as users_router

router = DefaultRouter()

router.registry.extend(assets_router.registry)
router.registry.extend(users_router.registry)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("consents.router")),
    path("docs/", include("docs.urls")),
]
