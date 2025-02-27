from consents.api.urls import router as consents_router
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api.urls import router as users_router

router = DefaultRouter()

router.registry.extend(consents_router.registry)
router.registry.extend(users_router.registry)


urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include("docs.urls")),
]
