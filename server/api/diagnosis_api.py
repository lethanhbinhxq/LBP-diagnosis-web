from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request
from typing import List
from sqlalchemy.orm import Session
from core.db_dependencies import get_db
from services.diagnosis_service import create_session_with_diagnoses, get_sessions_by_user, get_session_details, update_feedback
from core.auth_dependencies import get_current_user

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

@router.post("/run", status_code=200)
async def create_diagnosis_session(
    files: List[UploadFile] = File(...),
    texts: List[str] = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None  # add this
):
    if len(files) != len(texts):
        raise HTTPException(status_code=400, detail="Number of files and texts must match")

    user_id = int(current_user["sub"])

    try:
        session = await create_session_with_diagnoses(db, user_id, files, texts)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis processing failed: {str(e)}")

    base_url = str(request.base_url).rstrip("/")

    return {
        "session_id": session.id,
        "diagnoses": [
            {
                "diagnosis_id": d.id,
                "predicted_result": d.predicted_result,
                "report_text": d.report_text,
                "image_url": f"{base_url}/uploads/{d.image_path}" if d.image_path else None
            }
            for d in session.diagnoses
        ]
    }

@router.get("/sessions", status_code=200)
def list_diagnosis_sessions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    sessions = get_sessions_by_user(db, user_id)

    if not sessions:
        return {"sessions": []}

    return {"sessions": sessions}

@router.get("/sessions/{session_id}", status_code=200)
def get_session_by_id(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None,
):
    user_id = int(current_user["sub"])
    session = get_session_details(db, user_id, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    base_url = str(request.base_url).rstrip("/")

    # Attach absolute image URLs
    for diag in session["diagnoses"]:
        if diag["image_path"]:
            diag["image_url"] = f"{base_url}/uploads/{diag['image_path']}"
        else:
            diag["image_url"] = None

    return session

@router.put("/{diagnosis_id}/feedback")
def give_feedback(diagnosis_id: int, payload: dict, db: Session = Depends(get_db)):
    is_correct = payload.get("is_correct")
    comment = payload.get("comment")

    diagnosis = update_feedback(db, diagnosis_id, is_correct, comment)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    # return the updated diagnosis as plain dict
    return {
        "id": diagnosis.id,
        "predicted_result": diagnosis.predicted_result,
        "confidence_score": diagnosis.confidence_score,
        "is_correct": diagnosis.is_correct,
        "comment": diagnosis.comment,
        "image_path": diagnosis.image_path,
        "report_text": diagnosis.report_text,
    }