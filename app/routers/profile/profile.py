from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.common.database_conn import get_db
from app.common.model import User
from app.common.model import ProfileTable
from app.schemas.profile import ProfileUpdate, GenderEnum
from app.utils.cloudnary import upload_profile_image
from app.utils.security import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/create")
async def createProfile(name: Optional[str] = Form(None), 
    gender: Optional[GenderEnum] = Form(None),
    dateOfBirth: Optional[str] = Form(None),
    designation: str = Form(...),
    companyName: Optional[str] = Form(None),
    profileImageUrl: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),      
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
):

    user = db.query(User).filter(User.id == user_data.id).first()
   
    if not user:
        return {"error": "User not found"}
    profile=db.query(ProfileTable).filter(ProfileTable.userId ==user_data.id).first()
    if profile:
        return {"error": "Profile already exists"}
    if file:
        profile_image_path = await upload_profile_image(file)
    elif profileImageUrl:
        profile_image_path = profileImageUrl
    else:

        g = gender if gender is not None else profile.gender or "other"
        if g.lower() == "male":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794267/male_fu4acn.jpg"
        elif g.lower() == "female":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/female_rwr0am.jpg"
        else:
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/default_wjormw.png"
    
    if dateOfBirth:
        try:
            dateOfBirth = datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "dateOfBirth must be in YYYY-MM-DD format"}


    profileImage = profile_image_path
    print("profileImage:", profileImage)
    createProfile = ProfileTable(
        userId=user_data.id,
        name=user.name or name,
        email=user.email,
        phone=user.phone,
        gender=gender ,
        profileImage=profileImage,
        dateOfBirth=dateOfBirth,
        designation=designation,
        companyName=companyName,
        createdOn=user.createdOn
    )

    db.add(createProfile)
    db.commit()
    db.refresh(createProfile)

    return {"message": "Profile created successfully", "profile": createProfile}


# @router.put("/update")
# def update_profile(
#     gender: str = Form(None),
#     dateOfBirth: Optional[str] = Form(None),
#     designation: Optional[str] = Form(None),
#     companyName: Optional[str] = Form(None),
#     profileImage: Optional[UploadFile] = File(None), db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
  
#     profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()

#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     if profileImage:
#         if profileImage.content_type not in ["image/jpeg", "image/png"]:
#             raise HTTPException(status_code=400, detail="Invalid image type")
#         profile.profileImage = upload_profile_image(profileImage)

#     if gender is not None:
#         profile.gender = gender

#     if designation is not None:
#         profile.designation = designation

#     if companyName is not None:
#         profile.companyName = companyName

#     if dateOfBirth:
#         try:
#             profile.dateOfBirth = datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
#         except ValueError:
#             raise HTTPException(
#                 status_code=400,
#                 detail="dateOfBirth must be in YYYY-MM-DD format"
#             )

#     db.commit()
#     db.refresh(profile)

#     return {
#         "message": "Profile updated successfully",
#         "profile": profile
#     }

@router.put("/update-profile/")
async def update_profile(
    gender: Optional[GenderEnum] = Form(None),
    dateOfBirth: Optional[str] = Form(None),
    designation: Optional[str] = Form(None),
    companyName: Optional[str] = Form(None),
    profileImageUrl: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None),     
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
):
    profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
    if not profile:
        return {"error": "Profile not found"}
    
    if profileImageUrl and file:
        return {"error": "Please provide either a URL or a file, not both."}
    
    if file:
        profile_image_path = await upload_profile_image(file)
    elif profileImageUrl:
        profile_image_path = profileImageUrl

    else:
        g = gender if gender is not None else profile.gender or "other"
        if g.lower() == "male":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794267/male_fu4acn.jpg"
        elif g.lower() == "female":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/female_rwr0am.jpg"
        else:
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/default_wjormw.png"

    profile.gender = gender or profile.gender
    if dateOfBirth:
        try:
            profile.dateOfBirth = datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "dateOfBirth must be in YYYY-MM-DD format"}
    
    profile.designation = designation or profile.designation
    profile.companyName = companyName or profile.companyName
    profile.profileImage = profile_image_path

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "profile": {
            "userId": profile.userId,
            "name": profile.name,
            "email": profile.email,
            "phone": profile.phone,
            "gender": profile.gender,
            "dateOfBirth": profile.dateOfBirth,
            "designation": profile.designation,
            "companyName": profile.companyName,
            "profileImage": profile.profileImage,
            "createdOn": profile.createdOn,
            "updatedOn": profile.updatedOn
        }
    }


@router.get("/")
def get_profile(request: Request, db: Session = Depends(get_db),user_data: dict = Depends(get_current_user)  ):
    profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
   
    if not profile:
        return {"error": "Profile not found"}

    profile_image_url = profile.profileImage


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