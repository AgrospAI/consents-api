from typing import Self

from pydantic import BaseModel, field_serializer, model_validator

from consents_api.db import utils
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
    user_public_key: str

    @field_serializer("state", when_used="json")
    def serialize_consent_state(self, value: ConsentState) -> str:
        """Serializes the consent state to a string.

        :param value: consent state.
        :return: serialized consent state.
        :rtype: str
        """

        return value.name


class ConsentInputDTO(BaseModel):
    """DTO for creating new consent model."""

    asset_did: str
    asset_owner: str
    reason: str
    user_public_key: str

    def to_dto(self) -> ConsentDTO:
        """Converts the input DTO to the output DTO."""

        return ConsentDTO(
            asset_did=self.asset_did,
            asset_owner=self.asset_owner,
            reason=self.reason,
            state=ConsentState.PENDING,
            user=self.user_public_key,
        )

    @model_validator(mode="after")
    def validate_user_pk_length(self) -> Self:
        """Validates the length of the user public key.

        :raises ValueError: if the user public key is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """

        utils.validate_key_length(self.asset_owner)
        return self

    @model_validator(mode="after")
    def validate_asset_owner_length(self) -> Self:
        """Validates the length of the asset owner.

        :raises ValueError: if the asset owner is not 42 characters long.
        :return: self instance.
        :rtype: Self
        """

        utils.validate_key_length(self.user_public_key)
        return self
