from sqlalchemy import Column, Integer, String, DateTime
from .db_session import Base  # ← Импортируем Base из твоего db_session.py
import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
