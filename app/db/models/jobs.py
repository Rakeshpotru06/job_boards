from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, unique=True, index=True)
    location = Column(String, index=True)
