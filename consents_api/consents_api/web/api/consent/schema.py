from pydantic import BaseModel, ConfigDict

from consents_api.db.models.consents import ConsentState


class ConsentDTO(BaseModel):
    """
    DTO for consent models.

    It returned when accessing consent models from the API.
    """

    id: int
    asset_did: str
    asset_owner: str
    reason: str
    state: ConsentState
    user: str

    model_config = ConfigDict(from_attributes=True)


class ConsentInputDTO(BaseModel):
    """DTO for creating new consent model."""

    asset_did: str
    reason: str
    user_pk: str


class ConsentUpdateDTO(BaseModel):
    """DTO for updating a consent model."""

    state: ConsentState
