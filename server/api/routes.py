from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.diagnosis_service import process_diagnosis

router = APIRouter()

@router.post("/predict")
async def predict(image: UploadFile = File(...), text: str = Form(...)):
    result = await process_diagnosis(image, text)
    return JSONResponse(content={"diagnosis": result})
