from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, DateTime, Integer, String


@dataclass
class Lead(db.Model):
    id: int
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    __tablename__ = "leads_info"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=True)
    last_visit = Column(DateTime, nullable=True)
    visits = Column(Integer, nullable=True, default=1)
