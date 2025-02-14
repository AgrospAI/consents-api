from typing import override
from services.authentication import AuthenticationService

class PontusXAuthenticationService(AuthenticationService):

    def __init__(self, net: str) -> None:
        self._net = net

    @override
    def is_authenticated(self, *args, **kwargs) -> bool:
        # This is a placeholder for the actual implementation
        return True