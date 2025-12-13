from pydantic import BaseModel, Field

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback: str = Field(..., min_length=3)


class DummyUser:
    id = 5
    name = "Sam"
    designation = "HR"
    companyName = "IRT Solution"
    image = "https://example.com/profile.png"