from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db_connection import Base
from core.soft_delete import SoftDeleteMixin

class User(Base, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)

    # Relationships
    sessions = relationship("DiagnosisSession", back_populates="user", cascade="all, delete-orphan")