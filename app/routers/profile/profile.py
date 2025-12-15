from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.common.database_conn import get_db
from app.common.model import User
from app.common.model import ProfileTable
from app.schemas.profile import ProfileUpdate, GenderEnum
from app.utils.security import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/create")
def createProfile(data: ProfileUpdate,db: Session = Depends(get_db),user_data: dict = Depends(get_current_user)):

    user = db.query(User).filter(User.id == user_data.id).first()
   
    if not user:
        return {"error": "User not found"}
    profile=db.query(ProfileTable).filter(ProfileTable.userId ==user_data.id).first()
    if profile:
        return {"error": "Profile already exists"}
    print("data.profileImage:", data.gender)


    if data.profileImage: 
      print("fdd") 
      profileImage = data.profileImage
    else:  
      if data.gender and data.gender.value == "male":
        profileImage = "male.jpg"
      elif data.gender and data.gender.value == "female":
        profileImage = "female.jpg"
      else:
        print("default.png assigned")
        profileImage = "default.png"

    print("profileImage:", profileImage)
    createProfile = ProfileTable(
        userId=user_data.id,
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

    db.add(createProfile)
    db.commit()
    db.refresh(createProfile)

    return {"message": "Profile created successfully", "profile": createProfile}


@router.put("/update")
def update_profile(data: ProfileUpdate, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
  
    profile = (db.query(ProfileTable).filter(ProfileTable.userId == user_data.id) .first())

    if not profile:
        return {"error": "Profile not found"}

    if data.profileImage:
        profileImage = data.profileImage
    else:
        if data.gender and data.gender.value == "male":
            profileImage = "male.jpg"
        elif data.gender and data.gender.value == "female":
            profileImage = "female.jpg"
        else:
            profileImage = "default.png"

    profile.gender = data.gender
    profile.profileImage = profileImage
    profile.dateOfBirth = data.dateOfBirth
    profile.designation = data.designation
    profile.companyName = data.companyName

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "profile": profile
    }


@router.get("/")
def get_profile(request: Request, db: Session = Depends(get_db),user_data: dict = Depends(get_current_user)  ):
    profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
    if not profile:
        return {"error": "Profile not found"}
    print("profile.profileImage:", profile.profileImage)
    
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
