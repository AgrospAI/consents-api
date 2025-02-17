from typing import Annotated, Generator

from app.core.config import settings
from app.core.engine import engine
from app.services.auth import IAuthenticationService
from app.services.impl.auth import AuthenticationService
from app.services.impl.users import UsersService
from app.services.users import IUsersService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
UsersServiceDep = Annotated[IUsersService, Depends(UsersService)]
AuthServiceDep = Annotated[IAuthenticationService, Depends(AuthenticationService)]
