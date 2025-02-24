from django.urls import include, path

from rest_framework.routers import DefaultRouter

from consents.viewsets import ConsentsViewset
from users.viewsets import UsersViewset

router = DefaultRouter()


router.register(r"consents", ConsentsViewset, "consents")
router.register(r"users", UsersViewset, "users")

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include("docs.urls")),
]
