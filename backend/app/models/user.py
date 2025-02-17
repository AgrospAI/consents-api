from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.consent import Consent


class UserBase(SQLModel):
    public_key: str = Field(unique=True, index=True, primary_key=True)
    is_active: bool = True
    is_superuser: bool = False


# Database model, database table inferred from class name
class User(UserBase, table=True):
    consents: list[Consent] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    # password: str = Field(min_length=8, max_length=40)
    pass
