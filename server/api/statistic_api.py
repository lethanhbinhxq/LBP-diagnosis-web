from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.statistic_service import get_statistics
from core.db_dependencies import get_db

router = APIRouter(prefix="/statistics")

@router.get("/")
def fetch_statistics(db: Session = Depends(get_db)):
    """
    Returns both model pretraining metrics and real diagnosis history
    """
    stats = get_statistics(db)
    return stats
