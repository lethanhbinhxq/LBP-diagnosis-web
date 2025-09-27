from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.diagnosis_service import process_diagnosis, update_feedback, create_session

router = APIRouter(prefix="/diagnosis")

@router.post("/session")
async def new_session(user_id: int = Form(...)):
    session_id = await create_session(user_id)
    return {"session_id": session_id}

@router.post("/predict")
async def predict(
    session_id: int = Form(...),
    image: UploadFile = File(...),
    text: str = Form(...)
):
    result = await process_diagnosis(image, text, session_id)
    return JSONResponse(content=result)

class FeedbackRequest(BaseModel):
    diagnosis_id: int
    is_correct: bool
    comment: str | None = None

@router.post("/feedback")
async def feedback(request: FeedbackRequest):
    success = await update_feedback(request.diagnosis_id, request.is_correct, request.comment)
    if not success:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return {"message": "Feedback updated successfully"}
