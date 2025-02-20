from encodings import cp037
from typing import List

from consents_api.db.dao.user_dao import UserDAO
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from consents_api.db.dao.consent_dao import ConsentDAO
from consents_api.db.models.consents import Consent
from consents_api.web.api.consent.schema import ConsentDTO, ConsentInputDTO
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/consents",
    tags=["consents"],
)


@router.get(
    "/",
    response_model=List[ConsentDTO],
)
async def get_consent_models(
    limit: int = 10,
    offset: int = 0,
    consent_dao: ConsentDAO = Depends(),
) -> List[ConsentDTO]:
    """
    Retrieve all consent objects from the database.

    :param limit: limit of consent objects, defaults to 10.
    :param offset: offset of consent objects, defaults to 0.
    :param consent_dao: DAO for consent models.
    :return: list of consent objects from database.
    """

    consents = await consent_dao.get_consents(
        limit=limit,
        offset=offset,
    )

    return consents


@router.post(
    "/",
    response_model=ConsentDTO,
)
async def create_consent_model(
    new_consent_object: ConsentInputDTO,
    users_dao: UserDAO = Depends(),
    consent_dao: ConsentDAO = Depends(),
) -> ConsentDTO:
    """
    Creates consent model in the database.

    :param new_consent_object: new consent model item.
    :param consent_dao: DAO for consent models.
    """

    # Ensure that the owner & user exists in the database
    await users_dao.create_user(public_key=new_consent_object.asset_owner)
    await users_dao.create_user(public_key=new_consent_object.user_public_key)

    return await consent_dao.create_consent_model(consent_dto=new_consent_object)


@router.get(
    "/user/{public_key}",
    response_model=List[ConsentDTO],
)
async def retrieve_user_consents(
    public_key: str,
    limit: int = 10,
    offset: int = 0,
    consents_dao: ConsentDAO = Depends(),
) -> List[ConsentDTO]:
    """Retrieves the consents of the assets owned by {public_key}.

    :param limit: limit of consent objects, defaults to 10.
    :param offset: offset of consent objects, defaults to 0.
    :param consent_dao: DAO for consent models.
    :return: list of consent objects from database.
    """
    return await consents_dao.get_consents_by_asset_owner(
        asset_owner=public_key,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/asset/{asset_did}",
    response_model=List[ConsentDTO],
)
async def retrieve_asset_consents(
    asset_did: str,
    limit: int = 10,
    offset: int = 0,
    consents_dao: ConsentDAO = Depends(),
) -> List[ConsentDTO]:
    """Retrieves the consents of the assets owned by {public_key}.

    :param limit: limit of consent objects, defaults to 10.
    :param offset: offset of consent objects, defaults to 0.
    :param consent_dao: DAO for consent models.
    :return: list of consent objects from database.
    """
    return await consents_dao.filter(
        asset_did=asset_did,
        limit=limit,
        offset=offset,
    )


@router.delete(
    "/{consent_id}",
    response_model=ConsentDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Consent with the given ID not found."
        },
    },
)
async def delete_consent(
    consent_id: int,
    consent_dao: ConsentDAO = Depends(),
) -> ConsentDTO:
    """Deletes the consent with the given ID.

    :param consent_id: ID of the consent to delete.
    :param consent_dao: DAO for consent models.
    :return: deleted consent.
    """

    consent = await consent_dao.delete_consent(consent_id=consent_id)

    if consent is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Consent with id `{consent_id}` not found."},
        )

    return consent
