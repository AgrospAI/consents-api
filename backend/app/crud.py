from sqlmodel import Session, select

from app.models import User


def get_user_by_public_key(
    *,
    session: Session,
    public_key: str,
) -> User | None:
    statement = select(User).where(User.public_key == public_key)
    session_user = session.exec(statement).first()

    return session_user


def authenticate(
    *,
    session: Session,
    public_key: str,
) -> User | None:
    db_user = get_user_by_public_key(session=session, public_key=public_key)

    if not db_user:
        return None

    return db_user
