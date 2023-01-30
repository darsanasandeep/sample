import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.sql.functions import current_timestamp

from connections.database import Base


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    phonenumber = Column(String(100))
    role = Column(SmallInteger)
    created_at = Column(DateTime, default=current_timestamp())
