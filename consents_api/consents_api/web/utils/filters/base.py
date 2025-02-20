from abc import ABC, abstractmethod
from typing import Generator, Sequence, TypeVar

T = TypeVar("T")


class Specification(ABC, T):
    """Specification pattern interface.

    :param ABC: abstract class base
    :type ABC: ABC
    :param T: Type of the item to check
    :type T: T
    """

    @abstractmethod
    def is_satisfied_by(self, item: T) -> bool:
        """Check if the given item satisfies the specification.

        :param item: Item to check
        :type item: T
        :return: If the item satisfies the specification
        :rtype: bool
        """


class Filter(ABC, T):
    """Applies a filter to a sequence of items returing a generator to iterate through.

    :param T: Class of the items we want to filter.
    :type T: T
    """

    @abstractmethod
    def filter(
        self,
        items: Sequence[T],
        spec: Specification,
    ) -> Generator[T, None, None]:
        """Filter the given sequence of items.

        :param items: Items to filter
        :type items: Sequence[T]
        :param spec: Specification to filter by
        :type spec: Specification
        :yield: Filtered items.
        :rtype: Generator[T, None, None]
        """
