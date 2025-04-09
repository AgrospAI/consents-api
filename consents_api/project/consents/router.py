from rest_framework.routers import SimpleRouter

from consents import viewsets

router = SimpleRouter()

router.register(r"consents", viewsets.ConsentsViewset, "consents")
