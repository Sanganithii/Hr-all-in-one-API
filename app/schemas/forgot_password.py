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


# class VerifyOtpResetPassword(BaseModel):
#     email: EmailStr
#     otp: Annotated[str, StringConstraints(min_length=6, max_length=6)]
#     new_password: Annotated[str, StringConstraints(min_length=5)]