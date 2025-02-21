from typing import TYPE_CHECKING, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from consents_api.db.dependencies import get_db_session
from consents_api.db.models.users import User

if TYPE_CHECKING:
    from consents_api.web.api.users.schema import UserDTO


class UserDAO:
    """Class for accessing user objects."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ) -> None:
        self.session = session

    async def exists(
        self,
        *,
        public_key: str,
    ) -> bool:
        """Checks if a user with the given public key exists.

        :param public_key: public key of the user.
        :type public_key: str
        :return: True if the user exists, False otherwise.
        :rtype: bool
        """

        raw = await self.session.execute(
            select(User).where(User.public_key == public_key),
        )

        return raw.scalars().first() is not None

    async def get_users(self) -> List["UserDTO"]:
        """Retrieves all users data.

        :return: list of user data dtos.
        :rtype: List["UserDTO"]
        """

        raw = await self.session.execute(
            select(User).options(selectinload(User.incoming_consents)),
        )

        return raw.scalars().all()

    async def get_user(
        self,
        *,
        public_key: str,
    ) -> Optional["UserDTO"]:
        """Retrieves user data from the given public key.

        :param public_key: public key of the user.
        :type public_key: str
        :return: user data dto.
        :rtype: "UserDTO"
        """

        raw = await self.session.execute(
            select(User)
            .where(User.public_key == public_key)
            .options(selectinload(User.incoming_consents)),
        )

        return raw.scalars().first()

    async def get_or_create(
        self,
        *,
        public_key: str,
    ) -> "UserDTO":
        """Retrieves user data from the given public key or creates a new user object.

        :param public_key: public key of the user.
        :type public_key: str
        :return: user object.
        :rtype: User
        """

        user = await self.get_user(public_key=public_key)

        if not user:
            user = await self.create_user(public_key=public_key)

        return user

    async def create_user(
        self,
        *,
        public_key: str,
    ) -> Optional["UserDTO"]:
        """Creates a new user object.

        :param public_key: public key of the user.
        :type public_key: str
        :return: user object.
        :rtype: User
        """

        if await self.exists(public_key=public_key):
            return None

        user = User(public_key=public_key)

        self.session.add(user)

        return user

    async def delete_user(
        self,
        *,
        public_key: str,
    ) -> Optional["UserDTO"]:
        """Removes a user object from the database.

        :param public_key: public key of the user.
        :type public_key: str
        :return: user object or None if User is not in the database.
        :rtype: User | None
        """

        user = await self.get_user(public_key=public_key)

        if not user:
            return None

        await self.session.delete(user)

        return user
