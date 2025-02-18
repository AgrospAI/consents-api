from enum import IntEnum

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from consents_api.db.base import Base
from consents_api.db.models.users import User


class ConsentState(IntEnum):
    """Enumeration for consent state."""

    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class Consent(Base):
    """Model for consent representation."""

    __tablename__ = "consent"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asset_did: Mapped[str] = mapped_column(String(length=80))
    reason: Mapped[str] = mapped_column(String(length=600))
    state: Mapped[ConsentState]
    user_public_key: Mapped[str] = mapped_column(
        String,
        ForeignKey("user.public_key"),
    )
    # user: Mapped["User"] = relationship(back_populates="user.consents")
