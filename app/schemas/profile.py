from pydantic import BaseModel, Field, model_validator,model_validator,StringConstraints
from datetime import date, datetime
from typing import Optional, Annotated  
import re
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class ImageURL(BaseModel):
    url: str


class ProfileUpdate(BaseModel):
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z ]+$")
    ] = Field(description="User's full name (letters and spaces only, 2-50 chars)")
    gender:  Optional[GenderEnum] = None
    dateOfBirth: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    designation: str  
    companyName: Optional[str] = None
    profileImageUrl: Optional[str] = None 

    
    @model_validator(mode="before")
    @classmethod
    def validate_dob(cls, values):
        dob = values.get("dateOfBirth")
        if dob:
            # Parse string to date if needed
            if isinstance(dob, str):
                try:
                    dob = datetime.strptime(dob, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("dateOfBirth must be in YYYY-MM-DD format")
        
            today = date.today()
            if dob > today:
                raise ValueError("Date of birth cannot be in the future")

            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old")
            values["dateOfBirth"] = dob
        return values
    
    class Config:
        from_attributes = True