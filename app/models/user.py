import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    tier = Column(String, default=None)
    years = Column(Integer, default=None)
