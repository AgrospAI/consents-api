from typing import TYPE_CHECKING, Set

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from consents_api.db.base import Base

if TYPE_CHECKING:
    from consents_api.db.models.consents import Consent


class User(Base):
    """Represents a user entity."""

    __tablename__ = "user"

    public_key: Mapped[str] = mapped_column(String(length=80), primary_key=True)

    consents: Mapped[Set["Consent"]] = relationship(back_populates="user")
