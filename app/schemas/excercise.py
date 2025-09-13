from uuid import UUID

from pydantic import BaseModel


# for input purposes
class ExcerciseBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    muscle_group: str | None = None


# for creating a new Excercise
class Excercise(ExcerciseBase):
    id: UUID


class WorkoutBase(BaseModel):
    user_id: UUID
    excercise_id: UUID
    reps: int
    sets: int
    rest: int | None = None


class Workout(WorkoutBase):
    id: UUID
