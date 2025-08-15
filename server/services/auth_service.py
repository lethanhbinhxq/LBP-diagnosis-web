from sqlalchemy.orm import Session
from models.user import User
from core.dependencies import get_db
import bcrypt

async def signup_user(username: str, password: str):
    db: Session = next(get_db())

    # Check if username exists
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {"error": "Username already taken"}

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(username=username, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

async def login_user(username: str, password: str):
    db: Session = next(get_db())

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "Invalid username or password"}

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"error": "Invalid username or password"}

    # For now, just return a simple message (JWT later if needed)
    return {"message": "Login successful"}