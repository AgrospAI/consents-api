from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from consents_api.db.dependencies import get_db_session
from consents_api.db.models.consents import Consent, ConsentState


class ConsentDAO:
    """Class for accessing consent table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_consent_model(self, name: str) -> None:
        """
        Add single consent to session.

        :param name: name of a consent.
        """
        self.session.add(Consent(name=name))

    async def get_all_consents(self, limit: int, offset: int) -> List[Consent]:
        """
        Get all consent models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(Consent).limit(limit).offset(offset),
        )

        return list(raw_dummies.scalars().fetchall())

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
