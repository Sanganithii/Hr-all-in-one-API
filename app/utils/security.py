from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.common.database_conn import get_db
from app.common.model import User
from app.utils.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    print("Decoded payload:", payload)
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )
    return user