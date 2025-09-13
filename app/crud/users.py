from uuid import UUID, uuid4

from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(user: UserCreate, db: Session) -> User:
    try:
        db_user = User(
            id=uuid4(),
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            tier=user.tier,
            years=user.years,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to create a user {str(e)}",
        )


def get_user(id: UUID, db: Session) -> User:
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
        return user

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to fetch user {str(e)}",
        )


def update_user(id: UUID, user: UserCreate, db: Session):
    try:
        db.query(User).filter(User.id == id).update(
            {
                User.username: user.username,
                User.hashed_password: get_password_hash(user.password),
                User.tier: user.tier,
                User.years: user.years,
            }
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        db.rollback()

        if e == SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to update user {str(e)}",
        )


def delete_user(id: UUID, db: Session):
    try:
        db_user = db.query(User).filter(User.id == id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no such user in database",
            )
        db.delete(db_user)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to delete user {str(e)}",
        )
