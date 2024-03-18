from sqlalchemy import Column, String, Integer, DateTime, Boolean
from app.db.setup import Base

class Paste(Base):
    __tablename__ = 'pastes'
    
    id = Column(Integer, primary_key=True, index=True)
    shortlink = Column(String, index=True)
    expires_at = Column(DateTime)
    expired = Column(Boolean, default=False)
    created_at = Column(DateTime)
