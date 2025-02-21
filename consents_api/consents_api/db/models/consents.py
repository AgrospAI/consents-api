from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from consents_api.db.base import Base
from consents_api.db.models.consent_states import ConsentState
from consents_api.db.models.users import User


class Consent(Base):
    """Model for consent representation."""

    __tablename__ = "consent"

    asset_did: Mapped[str] = mapped_column(String(length=80), primary_key=True)
    reason: Mapped[str] = mapped_column(String(length=600))
    state: Mapped[ConsentState]

    solicitor_public_key: Mapped[str] = mapped_column(
        String,
        ForeignKey("user.public_key"),
        primary_key=True,
    )
    owner_public_key: Mapped[str] = mapped_column(
        String,
        ForeignKey("user.public_key"),
    )

    solicitor: Mapped["User"] = relationship(back_populates="incoming_consents")
    owner: Mapped["User"] = relationship(back_populates="outgoing_consents")
