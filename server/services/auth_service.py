from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from core.db_dependencies import get_db
import bcrypt

from core.jwt_handler import create_access_token   # import the token creator


async def signup_user(fullname: str, email: str, password: str):
    db: Session = next(get_db())

    # Check if email exists
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(
        fullname=fullname,
        email=email,
        password=hashed_password.decode('utf-8')
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT for the new user
    token_data = {"sub": str(new_user.id), "email": new_user.email}
    access_token = create_access_token(data=token_data)

    return {
        "message": "User registered successfully",
        # "user_id": new_user.id,
        "fullname": new_user.fullname,
        "access_token": access_token,
        "token_type": "bearer"
    }


async def login_user(email: str, password: str):
    db: Session = next(get_db())

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not registered"
        )

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token on login
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(data=token_data)

    return {
        "message": "Login successful",
        # "user_id": user.id,
        "fullname": user.fullname,
        "access_token": access_token,
        "token_type": "bearer"
    }
