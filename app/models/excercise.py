from sqlalchemy import UUID, Column, String

from app.db.session import Base


class Excercise(Base):
    __tablename__ = "excercises"

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    muscle_group = Column(String)
