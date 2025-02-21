from typing import Self

from pydantic import BaseModel, field_serializer, model_validator

from consents_api.db import utils
from consents_api.db.models.consents import ConsentState


class ConsentDTO(BaseModel):
    """
    DTO for consent models.

    It returned when accessing consent models from the API.
    """

    asset_did: str
    reason: str
    state: ConsentState
    solicitor_public_key: str
    owner_public_key: str

    @field_serializer("state", when_used="json")
    def serialize_state(self, state: ConsentState) -> str:
        """Serializes the consent state to a string.

        :param value: consent state.
        :return: serialized consent state.
        :rtype: str
        """

        return state.name


class ConsentInputDTO(BaseModel):
    """DTO for creating new consent model."""

    asset_did: str
    reason: str
    solicitor_public_key: str
    owner_public_key: str

    @model_validator(mode="after")
    def validate_solicitor_public_key_length(self) -> Self:
        """Validates the length of the solicitor public key.

        :raises ValueError: if the solicitor public key is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """

        utils.validate_key_length(self.solicitor_public_key)
        return self

    @model_validator(mode="after")
    def validate_owner_public_key_length(self) -> Self:
        """Validates the length of the asset owner.

        :raises ValueError: if the asset owner is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """

        utils.validate_key_length(self.owner_public_key)
        return self


class ConsentDeleteDTO(BaseModel):
    """DTO for deleting consent model."""

    asset_did: str
    solicitor_public_key: str

    @model_validator(mode="after")
    def validate_solicitor_public_key_length(self) -> Self:
        """Validates the length of the solicitor public key.

        :raises ValueError: if the solicitor public key is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """

        utils.validate_key_length(self.solicitor_public_key)
        return self
