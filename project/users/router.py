from rest_framework.routers import SimpleRouter

from users import viewsets

router = SimpleRouter()

router.register("users", viewsets.UsersViewset, basename="users")
router.register("auth/wallet", viewsets.WalletAuthViewset, basename="auth")
