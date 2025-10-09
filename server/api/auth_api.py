from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth_service import signup_user, login_user

router = APIRouter()
router = APIRouter(prefix="/auth")

class SignupRequest(BaseModel):
    fullname: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup", status_code=201)
async def signup(request: SignupRequest):
    return await signup_user(request.fullname, request.email, request.password)

@router.post("/login", status_code=200)
async def login(request: LoginRequest):
    return await login_user(request.email, request.password)