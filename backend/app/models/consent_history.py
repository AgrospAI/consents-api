import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.consent import Consent, ConsentState


class ConsentHistory(SQLModel, table=True):
    consent_id: uuid.UUID = Field(foreign_key="consent.id", primary_key=True)
    updated_state: "ConsentState" = Field(
        sa_column=SAEnum("ConsentState"),
        sa_column_kwargs={"nullable": False},
    )
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    consent: "Consent" = Relationship(back_populates="history")
