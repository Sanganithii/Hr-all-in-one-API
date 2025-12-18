from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.database_conn import get_db
from app.schemas.forgot_password import ForgotPasswordRequest, VerifyOtpResetPassword
from app.common.model import User, PasswordReset
from app.utils.sendotp_helper import generate_otp, pwd_context, send_otp_email

router = APIRouter(prefix="/forgot-password", tags=["Forgot Password"])

@router.post("/user/send-otp")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if user:
        
        otp = generate_otp()
        otp_hash = pwd_context.hash(otp)

        
        expires_at = datetime.utcnow() + timedelta(minutes=10)

        reset = PasswordReset(
            user_id=user.id,
            otp_hash=otp_hash,
            expires_at=expires_at
        )

        db.add(reset)
        db.commit()

        
        send_otp_email(user.email, otp)

    
    return {
        "message": "If the account exists, an OTP has been sent to the registered email"
    }


@router.post("/user/verify-otp-reset-password")
def verify_otp_and_reset_password(data: VerifyOtpResetPassword, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP or email"
        )

    
    reset = (
        db.query(PasswordReset).filter(PasswordReset.user_id == user.id, PasswordReset.is_used == False)
        .order_by(PasswordReset.created_at.desc()).first())

    if not reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    
    if reset.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )

    
    if not pwd_context.verify(data.otp, reset.otp_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    
    user.set_password(data.new_password)

    
    reset.is_used = True

    db.commit()

    return {"message": "Password reset successful"}
