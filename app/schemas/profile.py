from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime
from typing import Optional
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"




class ProfileUpdate(BaseModel):

    gender:  Optional[GenderEnum] = None
    dateOfBirth: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    designation: str  # required field
    companyName: Optional[str] = None
    profileImage: Optional[str] = None #= Field(default="default.png")  # default value

    
    @model_validator(mode="before")
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
            # Optional: check minimum age
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValueError("User must be at least 18 years old")
            values["dateOfBirth"] = dob
        return values
    
    class Config:
        from_attributes = True
    


