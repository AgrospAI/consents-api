from rest_framework.validators import ValidationError


class DidLengthValidator:
    def __init__(self, min_length: int = 71, max_length: int = 71) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value: int) -> None:
        if not self.min_length <= len(str(value)) <= self.max_length:
            raise ValidationError(
                f"DID must be [{self.min_length}, {self.max_length}] characters long"
            )

    def __repr__(self) -> str:
        return "%s(min=%i, max=%i)" % (
            self.__class__.__name__,
            self.min_length,
            self.max_length,
        )

    def deconstruct(self) -> tuple:
        # Required to make this serializable in Django migrations
        return (
            self.__class__.__module__ + "." + self.__class__.__name__,
            [],
            {"min_length": self.min_length, "max_length": self.max_length},
        )
