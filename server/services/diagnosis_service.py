import os
from uuid import uuid4
from typing import List
from fastapi import UploadFile, HTTPException
from PIL import Image
from sqlalchemy.orm import Session, joinedload
from models.diagnosis_session import DiagnosisSession
from models.diagnosis import Diagnosis
from models.medclip_model import MedClipHandler
from models.mlp_classifier import MLPClassifierHandler
from core.config import UPLOAD_DIR

# init ML models once
medclip_handler = MedClipHandler()
mlp_handler = MLPClassifierHandler()

async def create_session_with_diagnoses(
    db: Session,
    user_id: int,
    files: List[UploadFile],
    texts: List[str],
):
    # 1. Create session
    session = DiagnosisSession(user_id=user_id)
    db.add(session)
    db.flush()

    diagnoses_out = []

    for idx, (image_file, text) in enumerate(zip(files, texts)):
        try:
            # Save file
            ext = os.path.splitext(image_file.filename)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png"]:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

            filename = f"{uuid4()}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(await image_file.read())

            # Predict
            image_data = Image.open(file_path).convert("RGB")
            result = mlp_handler.predict(image_data, text)
            predicted_label = max(result, key=result.get)
            confidence_score = result[predicted_label]

            # Save diagnosis
            new_diag = Diagnosis(
                session_id=session.id,
                predicted_result=predicted_label,
                confidence_score=confidence_score,
                image_path=filename,
                report_text=text
            )
            db.add(new_diag)
            db.flush()
            diagnoses_out.append(new_diag)

        except HTTPException as e:
            raise e  # bubble up controlled error
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error on sample {idx+1}: {str(e)}")

    db.commit()
    db.refresh(session)
    return session

def get_diagnosis_summary():
    pass

def get_sessions_by_user(db: Session, user_id: int):
    """
    Return all diagnosis sessions for a given user.
    Each session includes count of diagnoses and creation time.
    """
    sessions = (
        db.query(DiagnosisSession)
        .options(joinedload(DiagnosisSession.diagnoses))  # eager load diagnoses
        .filter(DiagnosisSession.user_id == user_id)
        .order_by(DiagnosisSession.created_at.desc())
        .all()
    )

    return [
        {
            "id": s.id,
            "num_diagnoses": len(s.diagnoses),
            "created_at": s.created_at,
        }
        for s in sessions
    ]

def get_session_details(db: Session, user_id: int, session_id: int):
    """
    Fetch a session and its diagnoses for the given user.
    """
    session = (
        db.query(DiagnosisSession)
        .options(joinedload(DiagnosisSession.diagnoses))
        .filter(DiagnosisSession.user_id == user_id, DiagnosisSession.id == session_id)
        .first()
    )

    if not session:
        return None

    return {
        "id": session.id,
        "num_diagnoses": len(session.diagnoses),
        "created_at": session.created_at,
        "diagnoses": [
            {
                "id": d.id,
                "predicted_result": d.predicted_result,
                "confidence_score": d.confidence_score,
                "is_correct": d.is_correct,
                "feedback": d.comment,
                "image_path": d.image_path,
                "report_text": d.report_text,
            }
            for d in session.diagnoses
        ],
    }

def update_feedback(db: Session, diagnosis_id: int, is_correct: bool | None, comment: str | None):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diagnosis:
        return None
    
    diagnosis.is_correct = is_correct
    diagnosis.comment = comment
    db.commit()
    db.refresh(diagnosis)
    return diagnosis