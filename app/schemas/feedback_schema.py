from pydantic import BaseModel, Field

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback: str = Field(..., min_length=3)


