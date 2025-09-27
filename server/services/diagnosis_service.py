import os
from uuid import uuid4
from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from core.db_connection import SessionLocal
from models.medclip_model import MedClipHandler
from models.mlp_classifier import MLPClassifierHandler

# Init once
medclip_handler = MedClipHandler()
mlp_handler = MLPClassifierHandler()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_diagnosis(image_file: UploadFile, text: str, session_id: int):
    # Save uploaded image
    ext = os.path.splitext(image_file.filename)[1]
    filename = f"{uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await image_file.read())

    # Process embeddings + predict
    image_data = Image.open(file_path).convert("RGB")
    img_emb, text_emb = medclip_handler.encode(image_data, text)
    result = mlp_handler.predict(img_emb, text_emb)
    predicted_label = max(result, key=result.get)

    # Save to DB
    db: Session = SessionLocal()
    new_diag = Diagnosis(
        session_id=session_id,
        predicted_result=predicted_label,
        image_path=file_path,
        report_text=text
    )
    db.add(new_diag)
    db.commit()
    db.refresh(new_diag)
    db.close()

    return {
        "diagnosis": result,
        "diagnosis_id": new_diag.id
    }

async def update_feedback(diagnosis_id: int, is_correct: bool, comment: str | None = None):
    db = SessionLocal()
    diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diag:
        return False
    diag.is_correct = is_correct
    diag.comment = comment
    db.commit()
    db.close()
    return True
