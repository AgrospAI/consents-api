from django.forms import ValidationError


class BitFieldMarked:
    def __init__(self, template: int) -> None:
        self._template = int(template)

    def __call__(self, value: int) -> None:
        # Check if any of the value bits are not marked in the base template
        if int(value) & ~self._template:
            raise ValidationError(
                f"Given bitfield {value} has bits not marked in required {self._template}"
            )

    def __repr__(self) -> str:
        return "%s(template=%i)" % (
            self.__class__.__name__,
            self._template,
        )

    def deconstruct(self) -> tuple:
        # Required to make this serializable in Django migrations
        return (
            self.__class__.__module__ + "." + self.__class__.__name__,
            [],
            {"template": self._template},
        )
