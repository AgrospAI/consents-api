from operator import attrgetter
from typing import Literal, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    RUNTIME: Literal["Development", "Production", "Testing"] = "Development"

    DATABASE_URI: str = "postgresql://postgres:example@db:5432/consents"
    AQUARIUS_URL: str = "https://aquarius.pontus-x.eu"  # Default to public Aquarius

    TEST_PRIVATE_KEY: str | None = Field(default=None)
    TEST_DATASET_DID: str | None = Field(default=None)
    TEST_ALGORITHM_DID: str | None = Field(default=None)

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

        assert self.AQUARIUS_URL, "AQUARIUS_URL must be set"

        return self


config = Config()
