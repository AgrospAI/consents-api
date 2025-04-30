from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from consents.viewsets import ConsentResponseViewset, ConsentsViewset

router = SimpleRouter()

router.register(
    r"consents",
    ConsentsViewset,
    "consents",
)


responses_router = NestedSimpleRouter(
    router,
    r"consents",
    lookup="consent",
)

responses_router.register(
    r"response",
    ConsentResponseViewset,
    "consent-response",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(responses_router.urls)),
]
