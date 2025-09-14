from typing import Sequence
from uuid import UUID, uuid4

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.excercises import excercise_not_found_error, user_not_found_error
from app.models.excercise import Excercise
from app.models.user import User
from app.models.workout import Workout
from app.schemas.excercise import WorkoutBase

workout_not_found_error = "workout not found"


def create_workout(workout: WorkoutBase, db: Session) -> Workout:
    try:
        # check if user exists
        db_user = db.query(User).filter(User.id == workout.user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=user_not_found_error,
            )

        # check if excercise exists or tell user to create one
        db_excercise = (
            db.query(Excercise)
            .filter(Excercise.id == workout.excercise_id)
            .first()
        )
        if db_excercise is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=excercise_not_found_error,
            )

        db_workout = Workout(
            user_id=workout.user_id,
            excercise_id=workout.excercise_id,
            reps=workout.reps,
            sets=workout.sets,
            rest=workout.rest,
        )
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        return db_workout

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unablet to create collection {str(e)}",
        )


def get_workout(w_id: UUID, db: Session) -> Workout:
    try:
        db_workout = db.query(Workout).filter(Workout.id == w_id).first()
        if db_workout is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=workout_not_found_error,
            )

        return db_workout

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to fetch workout {str(e)}",
        )


def get_workouts(user_id: UUID, db: Session) -> Sequence[Workout]:
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=user_not_found_error,
            )

        stmt = select(Workout).where(Workout.user_id == user_id)

        workouts = db.execute(stmt).scalars().all()

        return workouts

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to fetch workouts {str(e)}",
        )


def update_workout(w_id: UUID, workout: WorkoutBase, db: Session):
    try:
        db_user = db.query(User).filter(User.id == workout.user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=user_not_found_error,
            )

        db.query(Workout).filter(Workout.id == w_id).update(
            {
                Workout.reps: workout.reps,
                Workout.sets: workout.sets,
                Workout.rest: workout.rest,
            }
        )
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to update workout {str(e)}",
        )


def delete_workout(w_id: UUID, db: Session):
    try:
        db_workout = db.query(Workout).filter(Workout.id == w_id).delete()
        if db_workout == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=excercise_not_found_error,
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to delete workout {str(e)}",
        )
