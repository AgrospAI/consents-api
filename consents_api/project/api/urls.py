from django.urls import include, path

from rest_framework.routers import DefaultRouter

from consents.viewsets import AssetsViewset, ConsentsViewset
from users.viewsets import UsersViewset

router = DefaultRouter()

router.register(r"assets", AssetsViewset, "assets")
router.register(r"consents", ConsentsViewset, "consents")
router.register(r"users", UsersViewset, "users")

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include("docs.urls")),
]
