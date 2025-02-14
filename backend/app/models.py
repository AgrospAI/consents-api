from datetime import datetime
from enum import IntEnum
import uuid
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    public_key: str = Field(unique=True, index=True, primary_key=True)
    is_active: bool = True
    is_superuser: bool = False


# Database model, database table inferred from class name
class User(UserBase, table=True):
    consents: list["Consent"] = Relationship(back_populates="user", cascade_delete=True)


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
    state: ConsentState = Field(default=ConsentState.PENDING)


class ConsentCreate(ConsentBase):
    pass


class Consent(ConsentBase, table=True):
    user_public_key: str = Field(
        foreign_key="user.id",
        nullable=False,
        ondelete="CASCADE",
    )
    user: User | None = Relationship(back_populates="consents")
    state: ConsentState = Field(default=ConsentState.PENDING)


class ConsentHistory(SQLModel, table=True):
    consent_id: int = Field(foreign_key="consent.id", primary_key=True)
    updated_state: ConsentState = Field()
    updated_at: datetime = Field(default=datetime.now(datetime.timezone.utc))
    consent: Consent | None = Relationship(back_populates="history")


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
