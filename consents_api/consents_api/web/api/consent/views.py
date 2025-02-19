from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from consents_api.db.dao.consent_dao import ConsentDAO
from consents_api.db.models.consents import Consent
from consents_api.web.api.consent.schema import ConsentDTO, ConsentInputDTO

router = APIRouter(
    prefix="/consents",
    tags=["consents"],
)


@router.get("/", response_model=List[ConsentDTO])
async def get_consent_models(
    limit: int = 10,
    offset: int = 0,
    consent_dao: ConsentDAO = Depends(),
) -> List[Consent]:
    """
    Retrieve all consent objects from the database.

    :param limit: limit of consent objects, defaults to 10.
    :param offset: offset of consent objects, defaults to 0.
    :param consent_dao: DAO for consent models.
    :return: list of consent objects from database.
    """
    return await consent_dao.get_all_consents(limit=limit, offset=offset)


@router.get("/{address}", response_model=List[ConsentDTO])
async def retrieve_consent(
    address: str,
    limit: int = 10,
    offset: int = 0,
    consents_dao: ConsentDAO = Depends(),
) -> List[Consent]:
    """Retrieves the consents of the assets owned by {address}.

    :param limit: limit of consent objects, defaults to 10.
    :param offset: offset of consent objects, defaults to 0.
    :param consent_dao: DAO for consent models.
    :return: list of consent objects from database.
    """
    return await consents_dao.get_consents(
        asset_owner=address,
        limit=limit,
        offset=offset,
    )


@router.post("/")
async def create_consent_model(
    new_consent_object: ConsentInputDTO,
    consent_dao: ConsentDAO = Depends(),
) -> None:
    """
    Creates consent model in the database.

    :param new_consent_object: new consent model item.
    :param consent_dao: DAO for consent models.
    """
    await consent_dao.create_consent_model(new_consent_object)
