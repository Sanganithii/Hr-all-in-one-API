import os
import secrets
import requests
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

def generate_otp():
    return str(secrets.randbelow(10**6)).zfill(6)


def send_otp_email(to_email: str, otp: str):
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("EMAIL_FROM", "no-reply@yourapp.com")

    if not sendgrid_api_key:
        raise RuntimeError("SENDGRID_API_KEY is not set")

    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": "Password Reset OTP"
            }
        ],
        "from": {"email": from_email},
       
        "content": [
    {
        "type": "text/plain",
        "value": (
            "Hello,\n\n"
            "You have a request to reset the password for your account.\n\n"
            f"Your One-Time Password (OTP) is: {otp}\n\n"
            "This OTP is valid for 10 minutes.\n"
            "For your security, please do not share this code with anyone.\n\n"
            "If you did not request a password reset, you can safely ignore this email.\n\n"
           
        )
    }
]
    }

    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(SENDGRID_URL, json=payload, headers=headers, timeout=30)

    if response.status_code not in (200, 202):
        raise RuntimeError(
            f"SendGrid email failed: {response.status_code} - {response.text}"
        )