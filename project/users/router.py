from rest_framework.routers import SimpleRouter

from users import viewsets

router = SimpleRouter()

router.register("users", viewsets.UsersViewset, basename="users")
