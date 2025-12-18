from pydantic import BaseModel, Field, StringConstraints, EmailStr
from typing_extensions import Annotated


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

