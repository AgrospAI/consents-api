from typing import TYPE_CHECKING, List, Self

from pydantic import BaseModel, Field, computed_field, model_validator

from consents_api.db import utils
from consents_api.db.models.consent_states import ConsentState

if TYPE_CHECKING:
    from consents_api.web.api.consent.schema import ConsentDTO


class UserDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    public_key: str
    incoming_consents: List["ConsentDTO"] = Field(exclude=True)
    outgoing_consents: List["ConsentDTO"] = Field(exclude=True)

    @computed_field
    @property
    def incoming_pending_consents(self) -> int:
        """Return the number of pending incoming consent petitions."""
        return len(
            [c for c in self.incoming_consents if c.state == ConsentState.PENDING],
        )

    @computed_field
    @property
    def outgoing_pending_consents(self) -> int:
        """Return the number of pending outgoing consent petitions."""
        return len(
            [c for c in self.outgoing_consents if c.state == ConsentState.PENDING],
        )


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
