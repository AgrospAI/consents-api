from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import User, UserCreate


class IUsersService(ABC):
    @abstractmethod
    def get_user_by_public_key(self, *, public_key: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_current_user(self) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, *, user_create: UserCreate) -> User:
        pass
