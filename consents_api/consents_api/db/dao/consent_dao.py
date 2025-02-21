from typing import TYPE_CHECKING, Any, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from consents_api.db.dependencies import get_db_session
from consents_api.db.models.consents import Consent, ConsentState
from consents_api.web.api.consent.schema import ConsentInputDTO

if TYPE_CHECKING:
    from consents_api.web.api.consent.schema import ConsentDTO


class ConsentDAO:
    """Class for accessing consent table."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ) -> None:
        self.session = session

    async def create_consent_model(
        self,
        *,
        consent_dto: ConsentInputDTO,
    ) -> "ConsentDTO":
        """Create a new consent model in the database.

        :param consent_dto: consent DTO.
        :type consent_dto: ConsentInputDTO
        :return: created consent model.
        :rtype: ConsentDTO
        """

        consent = Consent(
            asset_did=consent_dto.asset_did,
            reason=consent_dto.reason,
            state=ConsentState.PENDING,
            solicitor_public_key=consent_dto.solicitor_public_key,
            owner_public_key=consent_dto.owner_public_key,
        )

        self.session.add(consent)

        # Update consent's contents
        await self.session.flush()
        await self.session.refresh(consent, ["solicitor", "owner"])

        return consent

    async def get_consent(
        self,
        *,
        asset_did: str,
        solicitor_public_key: str,
    ) -> Optional["ConsentDTO"]:
        """Get a consent by its identifiers.

        :param asset_did: consent asset identifier.
        :type asset_did: str
        :param solicitor_public_key: consent solicitor public key.
        :type solicitor_public_key: str
        :return: consent model dto or None if it doesn't exist.
        :rtype: ConsentDTO | None
        """

        raw = await self.session.execute(
            select(Consent)
            .where(Consent.asset_did == asset_did)
            .where(Consent.solicitor_public_key == solicitor_public_key)
            .limit(1)
            .options(selectinload(Consent.user)),
        )

        return raw.scalars().first()

    async def get_consents(
        self,
        *,
        limit: int,
        offset: int,
    ) -> List["ConsentDTO"]:
        """
        Get all consent models with limit/offset pagination.

        :param limit: limit of consents.
        :param offset: offset of consents.
        :return: stream of consent dtos.
        """

        raw = await self.session.execute(
            select(Consent)
            .options(selectinload(Consent.user))
            .limit(limit)
            .offset(offset),
        )

        return list(raw.scalars().all())

    async def delete_consent(
        self,
        *,
        asset_did: str,
        solicitor_public_key: str,
    ) -> Optional["ConsentDTO"]:
        """Deletes a consent from the database.

        :param consent_id: consent idetifier.
        :type consent_id: int
        :return: deleted consent dto or None if it doesn't exist.
        :rtype: ConsentDTO | None
        """

        consent = await self.get_consent(
            asset_did=asset_did,
            solicitor_public_key=solicitor_public_key,
        )

        if not consent:
            return None

        await self.session.delete(consent)

        return consent

    async def filter(
        self,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[Consent]:
        """Get specific consents with dynamic filtering and pagination.

        :param limit: Number of records to return (default 10).
        :param offset: Number of records to skip (default 0).
        :param kwargs: Dynamic filter arguments (e.g., state="PENDING").
        :return: List of consents matching filters.
        """

        query = select(Consent).options(selectinload(Consent.user))

        # Apply dynamic filters
        if kwargs:
            query = query.filter_by(**kwargs)

        # Apply pagination
        query = query.limit(limit).offset(offset)

        rows = await self.session.execute(query)

        return list(rows.scalars().all())
