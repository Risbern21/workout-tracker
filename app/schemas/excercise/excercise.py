from uuid import UUID

from pydantic import BaseModel


# for output purposes
class ExcerciseBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    muscle_group: str | None = None


# for creating a new Excercise
class Excercise(ExcerciseBase):
    id: UUID
