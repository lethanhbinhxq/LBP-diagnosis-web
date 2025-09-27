# models/diagnosis_session.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.db_connection import Base
from core.soft_delete import SoftDeleteMixin

class DiagnosisSession(Base, SoftDeleteMixin):
    __tablename__ = "diagnosis_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")
    diagnoses = relationship("Diagnosis", back_populates="session", cascade="all, delete-orphan")
