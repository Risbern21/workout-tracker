from operator import or_
from typing import Sequence
from uuid import UUID, uuid4

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.excercise import Excercise
from app.schemas.excercise import ExcerciseBase

user_not_found_error = "user does not exist"
excercise_not_found_error = "excercise does not exist"


def create_excercise(excercise: ExcerciseBase, db: Session) -> Excercise:
    try:
        db_excercise = Excercise(
            id=uuid4(),
            name=excercise.name,
            description=excercise.description,
            muscle_group=excercise.muscle_group,
            category=excercise.category,
        )

        db.add(db_excercise)
        db.commit()
        db.refresh(db_excercise)
        return db_excercise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to create excercise {str(e)}",
        )


def get_excercise(e_id: UUID, db: Session) -> Excercise:
    try:
        db_excercise = db.query(Excercise).filter(Excercise.id == e_id).first()
        if not db_excercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=excercise_not_found_error,
            )

        return db_excercise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to get excercise {str(e)}",
        )


def get_excercises(
    db: Session, search: str | None = None
) -> Sequence[Excercise]:
    try:
        if search is None:
            stmt = select(Excercise).limit(20)
        else:
            stmt = (
                select(Excercise)
                .where(
                    or_(
                        Excercise.name.ilike(f"%{search}%"),
                        Excercise.muscle_group.ilike(f"%{search}%"),
                    )
                )
                .limit(20)
            )

        excercises: Sequence[Excercise] = db.execute(stmt).scalars().all()
        return excercises

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to fetch excercises {str(e)}",
        )


def update_excercise(e_id: UUID, excercise: ExcerciseBase, db: Session):
    try:
        db_excercise = (
            db.query(Excercise)
            .filter(Excercise.id == e_id)
            .update(
                {
                    Excercise.name: excercise.name,
                    Excercise.description: excercise.description,
                    Excercise.category: excercise.category,
                    Excercise.muscle_group: excercise.muscle_group,
                }
            )
        )
        if db_excercise == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=excercise_not_found_error,
            )
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to update excercise {str(e)}",
        )


def delete_excercise(e_id: UUID, db: Session):
    try:
        db_excercise = db.query(Excercise).filter(Excercise.id == e_id).delete()
        if db_excercise is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=excercise_not_found_error,
            )
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to delete excercise {str(e)}",
        )
