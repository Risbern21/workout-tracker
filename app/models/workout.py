import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base
from app.models.excercise import Excercise
from app.models.user import User


class Workout(Base):
    __tablename__ = "workout"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    excercise_id = Column(UUID, ForeignKey(Excercise.id, ondelete="CASCADE"))
    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"))
    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    rest = Column(Integer)
