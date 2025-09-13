from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.user import User


class Excercise(Base):
    __tablename__ = "excercises"

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    muscle_group = Column(String)


class Workout(Base):
    __tablename__ = "workout"

    id = Column(UUID, primary_key=True)
    excercise_id = Column(UUID, ForeignKey(Excercise.id, ondelete="CASCADE"))
    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"))
    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    rest = Column(Integer)
