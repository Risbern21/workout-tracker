from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.crud import users
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def crete_user(user: UserCreate, db: Session = Depends(get_db)):
    return users.create_user(user=user, db=db)


@router.get("/me")
def get_user(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "tier": current_user.tier,
        "years": current_user.years,
    }


@router.put("/{u_id}")
def update_user(
    u_id: UUID,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return users.update_user(id=u_id, user=user, db=db)


@router.delete("/{u_id}")
def delete_user(
    u_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return users.delete_user(u_id=u_id, current_user=current_user, db=db)
