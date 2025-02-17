from typing import Optional

from app.models.user import User
from app.services.auth import IAuthenticationService


class AuthenticationService(IAuthenticationService):
    def __init__(self):
        from app.api.deps import SessionDep, UsersServiceDep

        self._session = SessionDep
        self._users_service = UsersServiceDep

    def authenticate(self, *, public_key: str) -> Optional[User]:
        db_user = self._users_service.get_user_by_public_key(
            session=self._session,
            public_key=public_key,
        )

        if not db_user:
            return None

        return db_user
