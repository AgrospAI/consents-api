from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import User


class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate(self, *, public_key: str) -> Optional[User]:
        pass
