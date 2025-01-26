from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    liters = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)