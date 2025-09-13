from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import excercises
from app.db.session import get_db
from app.schemas.excercise import ExcerciseBase

router = APIRouter(prefix="/excercises", tags=["excercises"])


@router.post("/create")
def create_excercise(excercise: ExcerciseBase, db: Session = Depends(get_db)):
    return excercises.create_excercise(excercise=excercise, db=db)


@router.get("/{e_id}")
def get_excercise(e_id: UUID, db: Session = Depends(get_db)):
    return excercises.get_excercise(e_id=e_id, db=db)


@router.get("/")
def get_excercises(search: str | None = None, db: Session = Depends(get_db)):
    return excercises.get_excercises(search=search, db=db)


@router.put("/{e_id}")
def update_excercise(
    e_id: UUID, excercise: ExcerciseBase, db: Session = Depends(get_db)
):
    return excercises.update_excercise(e_id=e_id, excercise=excercise, db=db)


@router.delete("/{e_id}")
def delete_excercise(e_id: UUID, db: Session = Depends(get_db)):
    return excercises.delete_excercise(e_id=e_id, db=db)
