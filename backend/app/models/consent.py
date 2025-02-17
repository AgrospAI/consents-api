import uuid
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from app.models.user import User


class ConsentState(IntEnum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class ConsentBase(SQLModel):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    user_public_key: str = Field(index=True)
    asset_did: str = Field(index=True)
    reason: str = Field(nullable=False)


class ConsentUpdate(ConsentBase):
    state: ConsentState = Field(
        sa_column=SAEnum(ConsentState),
        sa_column_kwargs={"nullable": False},
    )


class ConsentCreate(ConsentBase):
    pass


class Consent(ConsentBase, table=True):
    user_public_key: str = Field(
        foreign_key="user.id",
        nullable=False,
        ondelete="CASCADE",
    )
    user: "User" = Relationship(back_populates="consents")
    state: ConsentState = Field(sa_column_kwargs={"nullable": False})
