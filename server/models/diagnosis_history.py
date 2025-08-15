# models/diagnosis_history.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.db_connection import Base

class DiagnosisHistory(Base):
    __tablename__ = 'diagnosis_history'

    id = Column(Integer, primary_key=True, index=True)
    predicted_result = Column(String)  # e.g., 'LBP', 'No Finding'
    is_correct = Column(Boolean, default=None)  # User feedback: True/False/None
