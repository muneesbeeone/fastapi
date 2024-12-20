from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
