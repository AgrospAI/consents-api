from typing import Self

from pydantic import BaseModel, computed_field, model_validator

from consents_api.db import utils
from consents_api.db.models.consent_states import ConsentState
from consents_api.web.api.consent.schema import ConsentDTO


class UserDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    public_key: str
    consents: list["ConsentDTO"]

    @computed_field
    @property
    def pending_consents(self) -> int:
        """Return the number of pending consents."""
        return len([c for c in self.consents if c.state == ConsentState.PENDING])

    @computed_field
    @property
    def total_consents(self) -> int:
        """Return the total number of consents."""
        return len(self.consents)


class UserInputDTO(BaseModel):
    """DTO for creating new user model."""

    public_key: str

    @model_validator(mode="after")
    def validate_public_key_length(self) -> Self:
        """Validates the length of the public key.

        :raises ValueError: if the public key is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """
        utils.validate_key_length(self.public_key)
        return self
