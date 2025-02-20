from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status

from consents_api.db.dao.user_dao import UserDAO
from consents_api.web.api.users.schema import UserDTO, UserInputDTO
from consents_api.web.utils.message import Message

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=list[UserDTO],
)
async def retrieve_users(
    users_dao: UserDAO = Depends(),
) -> list[UserDTO]:
    """Retrieves all users data.

    :return: list of users data.
    :rtype: list[UserDTO]
    """

    users = await users_dao.get_users()

    return users


@router.get(
    "/{public_key}",
    response_model=UserDTO,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def retrieve_user(
    public_key: str,
    users_dao: UserDAO = Depends(),
) -> UserDTO:
    """Retrieves user data from the given public key.

    :param user_in: required user information.
    :type user_in: str
    :return: user data.
    :rtype: UserDTO
    """

    user = await users_dao.get_user(
        public_key=public_key,
    )

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User with address `{public_key}` not found"},
        )

    return user


@router.post(
    "/",
    response_model=UserDTO,
    responses={status.HTTP_409_CONFLICT: {"model": Message}},
)
async def create_user(
    user_in: UserInputDTO,
    users_dao: UserDAO = Depends(),
) -> UserDTO:
    """Creates a user instance.

    :param user_in: user information.
    :type user_in: UserInputDTO
    :return: created user data.
    :rtype: UserDTO
    """

    user = await users_dao.create_user(public_key=user_in.public_key)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": f"User with address `{user_in.public_key}` already exists"
            },
        )

    return user


@router.delete(
    "/{public_key}",
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def delete_user(
    public_key: str,
    users_dao: UserDAO = Depends(),
) -> UserDTO:
    """Deletes a user instance.

    :param public_key: public key of the user.
    :type public_key: str
    :return: deleted user
    :rtype: UserDTO
    """

    user = await users_dao.delete_user(public_key=public_key)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User with address `{public_key}` not found"},
        )

    return user
