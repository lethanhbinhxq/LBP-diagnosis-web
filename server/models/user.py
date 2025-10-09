from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from core.db_connection import Base
from core.soft_delete import SoftDeleteMixin

class User(Base, SoftDeleteMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    sessions = relationship("DiagnosisSession", back_populates="user", cascade="all, delete-orphan")