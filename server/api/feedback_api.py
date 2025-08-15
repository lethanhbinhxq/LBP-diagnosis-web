from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services.email_service import send_feedback_email

router = APIRouter()

class FeedbackRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    message: str

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        await send_feedback_email(feedback.name, feedback.email, feedback.message)
        return {"message": "Feedback sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send feedback")
