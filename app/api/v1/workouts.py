from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.crud import workouts
from app.db.session import get_db
from app.models.user import User
from app.schemas.excercise import WorkoutBase

router = APIRouter(prefix="/workouts")


@router.post("/")
def add_workout(
    workout: WorkoutBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return workouts.create_workout(workout=workout, db=db)


@router.get("/{w_id}")
def get_my_workout(
    w_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return workouts.get_workout(w_id=w_id, db=db)


@router.get("/my_workouts/{u_id}")
def get_my_workouts(
    u_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return workouts.get_workouts(user_id=u_id, db=db)


@router.put("/{w_id}")
def update_my_workout(
    w_id: UUID,
    workout: WorkoutBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return workouts.update_workout(w_id=w_id, workout=workout, db=db)


@router.delete("/{w_id}")
def delete_my_workout(
    w_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return workouts.delete_workout(w_id=w_id, db=db)
