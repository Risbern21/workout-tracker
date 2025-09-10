from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import users
from app.db.session import get_db
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def crete_user(user: UserCreate, db: Session = Depends(get_db)):
    return users.create_user(user=user, db=db)


@router.get("/{id}")
def get_user(id: UUID, db: Session = Depends((get_db))):
    return users.get_user(id=id, db=db)


@router.put("/{id}")
def update_user(id: UUID, user: UserCreate, db: Session = Depends(get_db)):
    return users.update_user(id=id, user=user, db=db)


@router.delete("/{id}")
def delete_user(id: UUID, db: Session = Depends(get_db)):
    return users.delete_user(id=id, db=db)
