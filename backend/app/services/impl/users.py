from typing import Optional

import jwt
from app.core import security
from app.core.config import settings
from app.models.token import TokenPayload
from app.models.user import User, UserCreate
from app.services.users import IUsersService
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select


class UsersService(IUsersService):
    def __init__(self):
        from app.api.deps import SessionDep, TokenDep

        self._session = SessionDep
        self._token = TokenDep

    def get_user_by_public_key(
        self,
        *,
        public_key: str,
    ) -> Optional[User]:
        statement = select(User).where(User.public_key == public_key)
        session_user = self._session.exec(statement).first()

        return session_user

    def get_current_user(self) -> User:
        try:
            payload = jwt.decode(
                self._token,
                settings.SECRET_KEY,
                algorithms=[security.ALGORITHM],
            )
            token_data = TokenPayload(**payload)
        except (InvalidTokenError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

        user = self._session.get(User, token_data.sub)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )

        return user

    def create_user(self, user_create: UserCreate) -> User:
        db_obj = User.model_validate(user_create)

        self._session.add(db_obj)
        self._session.commit()
        self._session.refresh(db_obj)
        return db_obj
