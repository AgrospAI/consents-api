from datetime import datetime
from enum import IntEnum
from uuid import UUID

from base import Base
from sqlalchemy import Field


class ConsentPetitionState(IntEnum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class ConsentPetition(Base):
    user_did: str = Field(
        default=None,
        index=True,
    )

    asset_did: str = Field(
        default=None,
    )

    reason: str = Field(
        default=None,
        nullable=False,
    )

    state: ConsentPetitionState = Field(
        default=ConsentPetitionState.PENDING,
    )


class ConsentPetitionStateHistory(Base):
    consent_petition_uuid: UUID = Field(
        default=None,
        index=True,
    )

    updated_state: ConsentPetitionState = Field(
        default=None,
    )

    updated_at: datetime = Field(
        default=datetime.now(datetime.timezone.utc),
    )
