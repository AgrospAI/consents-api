from app.core.config import settings
from app.models.user import User, UserCreate
from app.api.deps import UsersServiceDep
from sqlmodel import Session, select


def init_db(
    session: Session,
    users_service: UsersServiceDep,
) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.public_key == settings.FIRST_SUPERUSER)
    ).first()

    if not user:
        user_in = UserCreate(
            public_key=settings.FIRST_SUPERUSER,
            is_superuser=True,
        )
        user = users_service.create_user(session=session, user_create=user_in)
