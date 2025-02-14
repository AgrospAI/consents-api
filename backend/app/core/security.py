from datetime import datetime, timedelta
from time import timezone
from typing import Any

import jwt
from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta,
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
