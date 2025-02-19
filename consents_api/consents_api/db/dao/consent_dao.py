from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from consents_api.db.dependencies import get_db_session
from consents_api.db.models.consents import Consent, ConsentState
from consents_api.web.api.consent.schema import ConsentDTO


class ConsentDAO:
    """Class for accessing consent table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_consent_model(self, consent_dto: ConsentDTO) -> None:
        """
        Add single consent to session.

        :param name: name of a consent.
        """
        self.session.add(
            Consent(
                asset_did=consent_dto.asset_did,
                asset_owner=consent_dto.asset_owner,
                reason=consent_dto.reason,
                state=consent_dto.state,
                user_public_key=consent_dto.user,
            )
        )

    async def get_all_consents(self, limit: int, offset: int) -> List[Consent]:
        """
        Get all consent models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw = await self.session.execute(
            select(Consent).limit(limit).offset(offset),
        )

        return list(raw.scalars().fetchall())

    async def get_consents(
        self,
        asset_owner: str,
        limit: int,
        offset: int,
    ) -> List[Consent]:
        """
        Get all consent models of owner with limit/offset pagination.

        :param asset_owner: owner of the consent.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """

        raw = await self.session.execute(
            select(Consent)
            .where(Consent.asset_owner == asset_owner)
            .limit(limit)
            .offset(offset),
        )

        return list(raw.scalars().fetchall())

    async def filter(self, state: Optional[ConsentState] = None) -> List[Consent]:
        """
        Get specific consent.

        :param state: state of consent instance.
        :return: consent models.
        """
        query = select(Consent)
        if state:
            query = query.where(Consent.state == state)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
