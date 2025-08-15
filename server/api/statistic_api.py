from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db
from services.diagnosis_service import get_diagnosis_summary

router = APIRouter(prefix="/statistic")

@router.get("/diagnosis_history")
def fetch_diagnosis_summary(db: Session = Depends(get_db)):
    summary = get_diagnosis_summary(db)
    return summary