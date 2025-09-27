from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth_service import signup_user, login_user

router = APIRouter()
router = APIRouter(prefix="/auth")

class SignupRequest(BaseModel):
    fullname: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    result = await signup_user(request.fullname, request.username, request.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
    
@router.post("/login")
async def login(request: LoginRequest):
    result = await login_user(request.username, request.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result