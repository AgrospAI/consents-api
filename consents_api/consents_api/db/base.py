from sqlalchemy.orm import DeclarativeBase

from consents_api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
