from sqlalchemy import Column, Integer, String, DateTime, JSON
from .db_session import Base
import datetime


class Cycle(Base):
    __tablename__ = 'cycless'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    user = Column(String(50), nullable=False)
    days_count = Column(Integer)
    descriptions = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self. name
