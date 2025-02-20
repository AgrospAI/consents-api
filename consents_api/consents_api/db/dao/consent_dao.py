from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from consents_api.db.dependencies import get_db_session
from consents_api.db.models.consents import Consent, ConsentState
from consents_api.web.api.consent.schema import ConsentInputDTO


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
    ) -> Consent:
        """
        Add single consent to session.

        :param name: name of a consent.
        """

        consent = Consent(
            asset_did=consent_dto.asset_did,
            asset_owner=consent_dto.asset_owner,
            reason=consent_dto.reason,
            state=ConsentState.PENDING,
            user_public_key=consent_dto.user_public_key,
        )

        self.session.add(consent)
        await self.session.flush()
        await self.session.refresh(consent, ["user"])  # Update consent's contents

        return consent

    async def get_consent(
        self,
        *,
        consent_id: int,
    ) -> Consent | None:
        """Get a consent by its identifier.

        :param consent_id: consent identifier.
        :type consent_id: int
        :return: consent model or None if it doesn't exist.
        :rtype: Consent | None
        """

        raw = await self.session.execute(
            select(Consent)
            .where(Consent.id == consent_id)
            .options(selectinload(Consent.user)),
        )

        return raw.scalars().first()

    async def get_consents(
        self,
        *,
        limit: int,
        offset: int,
    ) -> List[Consent]:
        """
        Get all consent models with limit/offset pagination.

        :param limit: limit of consents.
        :param offset: offset of consents.
        :return: stream of consents.
        """
        raw = await self.session.execute(
            select(Consent)
            .options(selectinload(Consent.user))
            .limit(limit)
            .offset(offset),
        )

        return list(raw.scalars().all())

    async def get_consents_by_asset_owner(
        self,
        *,
        asset_owner: str,
        limit: int,
        offset: int,
    ) -> List[Consent]:
        """
        Get all consent models of owner with limit/offset pagination.

        :param asset_owner: owner of the consent.
        :param limit: limit of consents.
        :param offset: offset of consents.
        :return: stream of consents.
        """

        raw = await self.session.execute(
            select(Consent)
            .where(Consent.asset_owner == asset_owner)
            .limit(limit)
            .offset(offset)
            .options(selectinload(Consent.user)),
        )

        return list(raw.scalars().all())

    async def filter(
        self,
        limit: int = 10,
        offset: int = 0,
        **kwargs,
    ) -> List[Consent]:
        """Get specific consents with dynamic filtering and pagination.

        :param limit: Number of records to return (default 10).
        :param offset: Number of records to skip (default 0).
        :param kwargs: Dynamic filter arguments (e.g., state="PENDING").
        :return: List of consents matching filters.
        """
        try:
            query = select(Consent).options(selectinload(Consent.user))

            # Apply dynamic filters
            if kwargs:
                query = query.filter_by(**kwargs)

            # Apply pagination
            query = query.limit(limit).offset(offset)

            rows = await self.session.execute(query)

            return list(rows.scalars().all())

        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    async def delete_consent(
        self,
        *,
        consent_id: int,
    ) -> Consent | None:
        """Deletes a consent from the database.

        :param consent_id: consent idetifier.
        :type consent_id: int
        :return: deleted consent or None if it doesn't exist.
        :rtype: Consent | None
        """

        consent = await self.get_consent(consent_id=consent_id)

        if not consent:
            return None

        await self.session.delete(consent)

        return consent
