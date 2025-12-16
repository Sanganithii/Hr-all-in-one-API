from pydantic import BaseModel, Field,EmailStr,constr,model_validator,StringConstraints
from typing import Optional, Annotated  
import re

from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, constr

class UserCreate(BaseModel):
    
    phone :Annotated[str, StringConstraints(pattern=r"^[6-9]\d{9}$")]
    email: Annotated[EmailStr,Field(..., description="Valid email address")]
    password : Annotated[str, StringConstraints(min_length=5)]

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[Annotated[str, StringConstraints(pattern=r"^[6-9]\d{9}$")]] = None
    old_password: Optional[str] = None
    new_password: Optional[Annotated[str, StringConstraints(min_length=5)]] = None
    

class Token(BaseModel):
    access_token: str
    token_type: str



class UserLogin(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User's email address")
    phone: Optional[str] = Field(None, description="User's phone number")
    password: str = Field(..., description="User's password")

    @model_validator(mode="after")
    def validate_login_identifier(self):
        if not self.email and not self.phone:
            raise ValueError("Either email or phone must be provided.")
        return self