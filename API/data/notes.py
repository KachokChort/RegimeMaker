from sqlalchemy import Column, Integer, String, DateTime, JSON
from .db_session import Base
import datetime


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    user = Column(String(50), nullable=False)
    descriptions = Column(String())
    start_at = Column(String(50))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name