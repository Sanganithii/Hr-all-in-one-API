from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta
from app.common.config import APIConfig

authcredential = APIConfig.AuthCredential()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=authcredential.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, authcredential.SECRET_KEY, algorithm=authcredential.ALGORITHM)


def decode_access_token(token: str):
    try:
        print("Decoding token:", token)
        return jwt.decode(token, authcredential.SECRET_KEY, algorithms=[authcredential.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
