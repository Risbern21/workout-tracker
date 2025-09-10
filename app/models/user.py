from sqlalchemy import UUID, Column, Integer, String

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    tier = Column(String, default=None)
    years = Column(Integer, default=None)
