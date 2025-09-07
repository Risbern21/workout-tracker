from sqlalchemy.orm import Session

from app.models.user.user import User
from app.schemas.user.user import UserCreate


def create_user(session: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username, email=user.email, hashed_password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
