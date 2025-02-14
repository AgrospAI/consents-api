from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Base(
    BaseModel,
    SQLModel,
    table=True,
):
    uuid: UUID = Field(
        default=None,
        primary_key=True,
    )

    created_at: datetime = Field(
        default=datetime.now(datetime.timezone.utc),
    )

    is_active: bool = Field(
        default=True,
    )
