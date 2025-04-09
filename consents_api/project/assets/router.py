from rest_framework.routers import SimpleRouter

from assets import viewsets

router = SimpleRouter()

router.register(r"assets", viewsets.AssetsViewset, "assets")
