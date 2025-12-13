from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.database_conn import get_db
from common.model import User
from common.model import ProfileTable
from schemas.profile import ProfileUpdate, GenderEnum
from fastapi import Request
from utils.security import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/create")
def update_profile(userId: int,data: ProfileUpdate,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == userId).first()
   
    if not user:
        return {"error": "User not found"}
    profile=db.query(ProfileTable).filter(ProfileTable.userId == userId).first()
    if profile:
        return {"error": "Profile already exists"}
    print("data.profileImage:", data.gender)
    # Set default profile image if none provided
    if data.profileImage: 
      print("fdd") # user uploaded image
      profileImage = data.profileImage
    else:  # set based on gender
      if data.gender and data.gender.value == "male":
        profileImage = "male.jpg"
      elif data.gender and data.gender.value == "female":
        profileImage = "female.jpg"
      else:
        print("default.png assigned")
        profileImage = "default.png"

    print("profileImage:", profileImage)
    updateProfile = ProfileTable(
        userId=userId,
        name=user.name,
        email=user.email,
        phone=user.phone,
        gender=data.gender,
        profileImage=profileImage,
        dateOfBirth=data.dateOfBirth,
        designation=data.designation,
        companyName=data.companyName,
        createdOn=user.createdOn
    )

    db.add(updateProfile)
    db.commit()
    db.refresh(updateProfile)

    return {"message": "Profile updated successfully", "profile": updateProfile}


@router.put("/create")
def update_profile(userId: int,data: ProfileUpdate,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == userId).first()
   
    if not user:
        return {"error": "User not found"}
    print("data.profileImage:", data.gender)
    # Set default profile image if none provided
    if data.profileImage: 
      print("fdd") # user uploaded image
      profileImage = data.profileImage
    else:  # set based on gender
      if data.gender and data.gender.value == "male":
        profileImage = "male.jpg"
      elif data.gender and data.gender.value == "female":
        profileImage = "female.jpg"
      else:
        print("default.png assigned")
        profileImage = "default.png"

    print("profileImage:", profileImage)
    updateProfile = ProfileTable(
        userId=userId,
        name=user.name,
        email=user.email,
        phone=user.phone,
        gender=data.gender,
        profileImage=profileImage,
        dateOfBirth=data.dateOfBirth,
        designation=data.designation,
        companyName=data.companyName,
        createdOn=user.createdOn
    )

    db.add(updateProfile)
    db.commit()
    db.refresh(updateProfile)

    return {"message": "Profile updated successfully", "profile": updateProfile}


# @router.get("/{userId}")
# def get_profile(userId: int, db: Session = Depends(get_db)):
#     profile = db.query(ProfileTable).filter(ProfileTable.userId == userId).first()
#     if not profile:
#         return {"error": "Profile not found"}

#     return {"profile": profile}




@router.get("/{userId}")
def get_profile(userId: int, request: Request, db: Session = Depends(get_db)):
    profile = db.query(ProfileTable).filter(ProfileTable.userId == userId).first()
    if not profile:
        return {"error": "Profile not found"}
    print("profile.profileImage:", profile.profileImage)
    # Build full URL for profile image
    profile_image_url = request.url_for("static", path=f"images/{profile.profileImage}")
    

    return {
        "profile": {
            "userId": profile.userId,
            "name": profile.name,
            "email": profile.email,
            "phone": profile.phone,
            "gender": profile.gender,
            "dateOfBirth": profile.dateOfBirth,
            "designation": profile.designation,
            "companyName": profile.companyName,
            "profileImage": profile_image_url,
            "createdOn": profile.createdOn,
            "updatedOn": profile.updatedOn
        }
    }
