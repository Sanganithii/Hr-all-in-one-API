from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.database_conn import get_db
from app.schemas.forgot_password import ForgotPasswordRequest, VerifyOtpRequest, ResetPasswordRequest
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
        "message": " OTP has been sent to the registered email",
        "note": "If you don’t see the email, please check your Spam or Junk folder."
    }


@router.post("/user/verify-otp")
def verify_otp(data: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or OTP"
        )

    reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False,
            PasswordReset.is_verified == False
        )
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

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

    reset.is_verified = True
    db.commit()

    return {"message": "OTP verified successfully"}


@router.post("/user/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email"
        )

    reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.user_id == user.id,
            PasswordReset.is_verified == True,
            PasswordReset.is_used == False
        )
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

    if not reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP verification required"
        )

    user.set_password(data.new_password)

    reset.is_used = True
    db.commit()

    return {"message": "Password reset successful"}
