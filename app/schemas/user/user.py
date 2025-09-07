from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Tier(str, Enum):
    beginner = "beginner"
    mid_beginner = "mid_beginner"
    intermediate = "intermediate"
    mid_intermediate = "mid_intermediate"
    advanced = "advanced"


# base user model only to be inherited
class UserBase(BaseModel):
    username: str
    email: EmailStr
    years: int | None = None
    tier: Tier | None = None


# for creating a user
class UserCreate(UserBase):
    password: str


# for outputting a user
class UserRead(UserBase):
    id: UUID

    # allows sqlalchemt objects to be converted automatically
    class Config:
        orm_mode = True
