from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from services.diagnosis_service import process_diagnosis
from pydantic import BaseModel
from services.diagnosis_service import update_feedback

router = APIRouter(prefix="/diagnosis")

@router.post("/predict")
async def predict(image: UploadFile = File(...), text: str = Form(...)):
    result = await process_diagnosis(image, text)
    return JSONResponse(content={"diagnosis": result})

class FeedbackRequest(BaseModel):
    diagnosis_id: int
    is_correct: bool

@router.post("/feedback")
async def feedback(request: FeedbackRequest):
    success = await update_feedback(request.diagnosis_id, request.is_correct)
    if not success:
        raise HTTPException(status_code=404, detail="Diagnosis record not found")
    return {"message": "Feedback updated successfully"}