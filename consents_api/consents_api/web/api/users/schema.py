from pydantic import BaseModel, ConfigDict, computed_field

from consents_api.web.api.consent.schema import ConsentDTO


class UserDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    public_key: str
    consents: list[ConsentDTO]

    @computed_field
    @property
    def pending_consents(self) -> int:
        """Return the number of pending consents."""
        return len([c for c in self.consents if c.status == "PENDING"])

    @computed_field
    @property
    def total_consents(self) -> int:
        """Return the total number of consents."""
        return len(self.consents)

    model_config = ConfigDict(from_attributes=True)


class UserInputDTO(BaseModel):
    """DTO for creating new user model."""

    public_key: str
