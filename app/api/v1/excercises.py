from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import excercises
from app.db.session import get_db
from app.models import excercise
from app.schemas.excercise import ExcerciseBase

router = APIRouter(prefix="/excercises", tags=["excercises"])


@router.post("/create")
def create_excercise(excercise: ExcerciseBase, db: Session = Depends(get_db)):
    return excercises.create_excercise(excercise=excercise, db=db)


@router.get("/{id}")
def get_excercise(id: UUID, db: Session = Depends(get_db)):
    return excercises.get_excercise(id=id, db=db)


@router.get("/")
def get_excercises(search: str | None = None, db: Session = Depends(get_db)):
    return excercises.get_excercises(search=search, db=db)
