from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

class Event(BaseModel):
    event_name: str
    event_status: str
    valid: bool

