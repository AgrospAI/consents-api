from datetime import datetime
from enum import IntEnum
from uuid import UUID
from base import Base


class ConsentPetitionState(IntEnum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

class ConsentPetition(Base):
    user_did: str
    asset_did: str
    reason: str
    state: ConsentPetitionState = ConsentPetitionState.PENDING


class ConsentPetitionStateHistory(Base):
    consent_petition_uuid: UUID
    updated_state: ConsentPetitionState
    updated_at: datetime