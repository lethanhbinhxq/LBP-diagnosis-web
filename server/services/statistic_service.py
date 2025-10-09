from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis, PredictedResultEnum
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def get_statistics(db: Session, user_id: int = None):
    """
    Compute metrics and history based on user feedback.
    Only include diagnoses with feedback for metric calculations.
    """
    # Fetch diagnoses
    query = db.query(Diagnosis)
    if user_id is not None:
        query = query.filter(Diagnosis.user_id == user_id)
    diagnoses = query.all()

    total = len(diagnoses)
    feedback_diagnoses = [d for d in diagnoses if d.is_correct is not None]
    feedback_given = len(feedback_diagnoses)
    no_feedback = total - feedback_given

    # Counts for history
    correct = len([d for d in feedback_diagnoses if d.is_correct])
    wrong = len([d for d in feedback_diagnoses if not d.is_correct])

    lbp_diagnoses = len([d for d in diagnoses if d.predicted_result == PredictedResultEnum.LBP])
    no_finding_diagnoses = len([d for d in diagnoses if d.predicted_result == PredictedResultEnum.NO_FINDING])

    correct_lbp = len([d for d in feedback_diagnoses if d.predicted_result == PredictedResultEnum.LBP and d.is_correct])
    wrong_lbp = len([d for d in feedback_diagnoses if d.predicted_result == PredictedResultEnum.LBP and not d.is_correct])

    correct_no_finding = len([d for d in feedback_diagnoses if d.predicted_result == PredictedResultEnum.NO_FINDING and d.is_correct])
    wrong_no_finding = len([d for d in feedback_diagnoses if d.predicted_result == PredictedResultEnum.NO_FINDING and not d.is_correct])

    # --- Compute model metrics based on your mapping ---
    y_pred = [1 if d.predicted_result == PredictedResultEnum.LBP else 0 for d in feedback_diagnoses]
    y_true = []
    for d in feedback_diagnoses:
        pred = 1 if d.predicted_result == PredictedResultEnum.LBP else 0
        if pred == 0:
            y_true.append(0 if d.is_correct else 1)
        else:  # pred == 1
            y_true.append(1 if d.is_correct else 0)

    if y_true:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
    else:
        accuracy = precision = recall = f1 = 0.0

    modelMetrics = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

    return {
        "modelMetrics": modelMetrics,
        "history": {
            "totalDiagnoses": total,
            "feedbackGiven": feedback_given,
            "noFeedback": no_feedback,
            "correctDiagnoses": correct,
            "wrongDiagnoses": wrong,
            "lbpDiagnoses": lbp_diagnoses,
            "noFindingDiagnoses": no_finding_diagnoses,
            "correctLbpDiagnoses": correct_lbp,
            "wrongLbpDiagnoses": wrong_lbp,
            "correctNoFindingDiagnoses": correct_no_finding,
            "wrongNoFindingDiagnoses": wrong_no_finding,
        }
    }
