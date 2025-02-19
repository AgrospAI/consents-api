from enum import IntEnum


class ConsentState(IntEnum):
    """Enumeration for consent state."""

    PENDING = 0

    ACCEPTED = 1

    REJECTED = 2
