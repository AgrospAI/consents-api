import logging

from app.api.deps import UsersServiceDep
from app.core.db import init_db
from app.core.engine import engine
from sqlmodel import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session=session, users_service=UsersServiceDep)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
