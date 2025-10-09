# models/diagnosis.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from core.db_connection import Base
from core.soft_delete import SoftDeleteMixin
import enum

class PredictedResultEnum(str, enum.Enum):
    LBP = "LBP"
    NO_FINDING = "No Finding"
    HERNIATION = "Herniation & Bulging"
    DEGENERATION = "Degeneration & Narrowing"
    BONY = "Bony Abnormalities"

class Diagnosis(Base, SoftDeleteMixin):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("diagnosis_session.id"), nullable=False)

    predicted_result = Column(
        Enum(PredictedResultEnum, name="predicted_result_enum"),
        nullable=False
    )

    confidence_score = Column(Float, nullable=False)
    
    is_correct = Column(Boolean, default=None)          # Feedback: True / False / None
    comment = Column(String, nullable=True)
    image_path = Column(String, nullable=False)          # Store image file path
    report_text = Column(String, nullable=False)         # Store radiology report text

    # Relationships
    session = relationship("DiagnosisSession", back_populates="diagnoses")
