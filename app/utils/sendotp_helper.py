import os
import secrets
import smtplib
from email.message import EmailMessage

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")

def generate_otp():
    return str(secrets.randbelow(10**6)).zfill(6)


def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = "no-reply@yourapp.com"
    msg["To"] = to_email

    msg.set_content(
        f"""
Your OTP for password reset is: {otp}

This OTP is valid for 10 minutes.
If you did not request this, please ignore this email.
        """
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)
