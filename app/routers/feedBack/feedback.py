from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.common.model import User
from app.utils.security import get_current_user
from app.common.model import ProfileTable, UserFeedback
from app.schemas.feedback_schema import FeedbackCreate
from app.common.database_conn  import get_db


router = APIRouter(prefix="/feedback", tags=["Feedback"])



@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_feedback(data:FeedbackCreate,db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    
    user=db.query(User).filter(User.id==current_user.id).first()
    existing_feedback = (
        db.query(UserFeedback)
        .filter(UserFeedback.userId == current_user.id)
        .first()
    )

    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feedback already submitted"
        )

   

    profile = (
        db.query(ProfileTable)
        .filter(ProfileTable.userId == current_user.id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=" profile is not updated"
        )
    if profile.designation is None or profile.designation.strip() == "":
        profile.designation = ""
    if profile.companyName is None or profile.companyName.strip() == "":
        profile.companyName = ""

        
    feedback = UserFeedback(
        userId=current_user.id,
        userName=profile.name,
        designation=profile.designation,
        companyName=profile.companyName,
        image=profile.profileImage,
        rating=data.rating,
        feedback=data.feedback
    )

    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "status": 201,
        "message": "Feedback submitted successfully"
    }


@router.get("/view-feedback")
def get_top_positive_feedback(db: Session = Depends(get_db)):
    
    rating_priority = [5, 4, 3,2,1]

    feedbacks = []
    selected_rating = None

    for rating in rating_priority:
        feedbacks = (
            db.query(UserFeedback)
            .filter(
                UserFeedback.rating == rating,
                UserFeedback.feedback.isnot(None),
                UserFeedback.feedback != ""
            )
            .order_by(UserFeedback.createdOn.desc())
            .limit(3)
            .all()
        )

        if feedbacks:
            selected_rating = rating
            break

    if not feedbacks:
        return {
            "message": "No feedback found",
            "data": []
        }

    return {
        "rating_used": selected_rating,
        "count": len(feedbacks),
        "data": [
            {
                "id": f.id,
                "image": f.image,
                "userName": f.userName,
                "designation": f.designation,
                "companyName": f.companyName,
                "rating": f.rating,
                "feedback": f.feedback,
                "createdOn": f.createdOn
            }
            for f in feedbacks
        ]
    }
