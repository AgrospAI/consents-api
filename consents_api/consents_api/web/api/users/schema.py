from pydantic import BaseModel, ConfigDict

from consents_api.web.api.consent.schema import ConsentDTO


class UserDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    public_key: str
    consents: list[ConsentDTO]

    model_config = ConfigDict(from_attributes=True)


class UserInputDTO(BaseModel):
    """DTO for creating new user model."""

    public_key: str
