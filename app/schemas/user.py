from pydantic import BaseModel, Field,EmailStr,constr,model_validator,StringConstraints
from typing import Optional, Annotated  
import re

from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, constr

class UserCreate(BaseModel):
    
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z ]+$")
    ] = Field(description="User's full name (letters and spaces only, 2-50 chars)")
    #name = Annotated[str, StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z ]+$")]
    phone :Annotated[str, StringConstraints(pattern=r"^[6-9]\d{9}$")]
    email: Annotated[EmailStr,Field(..., description="Valid email address")]
    password : Annotated[str, StringConstraints(min_length=5)]


    

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
