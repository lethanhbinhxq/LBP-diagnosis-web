from PIL import Image
from sqlalchemy.orm import Session
from models.medclip_model import MedClipHandler
from models.mlp_classifier import MLPClassifierHandler
from models.diagnosis_history import DiagnosisHistory
from core.db_connection import SessionLocal

# Initialize model handlers globally
medclip_handler = MedClipHandler()
mlp_handler = MLPClassifierHandler()

async def process_diagnosis(image_file, text):
    # Process image and predict
    image_data = Image.open(image_file.file).convert("RGB")
    img_emb, text_emb = medclip_handler.encode(image_data, text)
    result = mlp_handler.predict(img_emb, text_emb)  # e.g., 'LBP' or 'No Finding'
    predicted_label = max(result, key=result.get)

    # Save to database
    db: Session = SessionLocal()
    new_record = DiagnosisHistory(
        predicted_result=predicted_label
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return {
        "diagnosis": result,
        "record_id": new_record.id
    }

async def update_feedback(diagnosis_id: int, is_correct: bool):
    db = SessionLocal()
    record = db.query(DiagnosisHistory).filter(DiagnosisHistory.id == diagnosis_id).first()
    if not record:
        return False
    record.is_correct = is_correct
    db.commit()
    db.close()
    return True

def get_diagnosis_summary(db: Session):
    total = db.query(DiagnosisHistory).count()
    feedback_given = db.query(DiagnosisHistory).filter(DiagnosisHistory.is_correct != None).count()
    correct = db.query(DiagnosisHistory).filter(DiagnosisHistory.is_correct == True).count()
    wrong = db.query(DiagnosisHistory).filter(DiagnosisHistory.is_correct == False).count()

    lbp_total = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'LBP').count()
    no_finding_total = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'No Finding').count()

    correct_lbp = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'LBP', DiagnosisHistory.is_correct == True).count()
    wrong_lbp = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'LBP', DiagnosisHistory.is_correct == False).count()

    correct_no_finding = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'No Finding', DiagnosisHistory.is_correct == True).count()
    wrong_no_finding = db.query(DiagnosisHistory).filter(DiagnosisHistory.predicted_result == 'No Finding', DiagnosisHistory.is_correct == False).count()

    return {
        "totalDiagnoses": total,
        "feedbackGiven": feedback_given,
        "noFeedback": total - feedback_given,
        "correctDiagnoses": correct,
        "wrongDiagnoses": wrong,
        "lbpDiagnoses": lbp_total,
        "noFindingDiagnoses": no_finding_total,
        "correctLbpDiagnoses": correct_lbp,
        "wrongLbpDiagnoses": wrong_lbp,
        "correctNoFindingDiagnoses": correct_no_finding,
        "wrongNoFindingDiagnoses": wrong_no_finding
    }