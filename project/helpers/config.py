from operator import attrgetter
from typing import Literal, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    RUNTIME: Literal["Development", "Production", "Testing"] = "Development"

    DATABASE_URI: str

    TEST_PRIVATE_KEY: str | None
    TEST_DATASET_DID: str | None
    TEST_ALGORITHM_DID: str | None

    @model_validator(mode="after")
    def check_runtime(self) -> Self:
        match self.RUNTIME:
            case "Testing":

                def check_missing(property: str) -> None:
                    if not getattr(self, property):
                        raise ValueError(
                            f"Configuration property [{property}] must be set"
                        )

                    map(
                        check_missing,
                        attrgetter(
                            "TEST_PRIVATE_KEY", "TEST_DATASET_DID", "TEST_ALGORITHM_DID"
                        )(self),
                    )


config = Config()
