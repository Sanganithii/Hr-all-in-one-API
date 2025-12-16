from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.common.database_conn import get_db
from app.common.model import User
from app.common.model import ProfileTable
from app.schemas.profile import ProfileUpdate, GenderEnum
from app.utils.cloudnary import upload_profile_image, delete_profile_image
from app.utils.security import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


def validate_dob(dob_value):
    if dob_value:
        # Parse string to date if needed
        if isinstance(dob_value, str):
            try:
                dob_value = datetime.strptime(dob_value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("dateOfBirth must be in YYYY-MM-DD format")

        today = date.today()
        if dob_value > today:
            raise ValueError("Date of birth cannot be in the future")

        # Optional: check minimum age
        age = today.year - dob_value.year - ((today.month, today.day) < (dob_value.month, dob_value.day))
        if age < 18:
            raise ValueError("User must be at least 18 years old")
    return dob_value

@router.post("/create")
async def createProfile(name: str = Form(...), 
    gender: Optional[GenderEnum] = Form(None),
    dateOfBirth: Optional[date] = Form(None),
    designation: str = Form(...),
    companyName: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),      
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
):  
    if gender == "":
       gender = None
    if dateOfBirth == "":
       dateOfBirth = None
    
    if companyName == "":
       companyName = None
    if dateOfBirth is not None:
       try:
           dateOfBirth_valid = validate_dob(dateOfBirth)
       except ValueError as e:
           raise HTTPException(status_code=422, detail=str("invalid dateOfBirth: " + str(e)))
    
    
    user = db.query(User).filter(User.id == user_data.id).first()
    if not user:
        return {"error": "User not found"}
    profile=db.query(ProfileTable).filter(ProfileTable.userId ==user_data.id).first()
    if profile:
        return {"error": "Profile already exists"}
    
    if file:
        profile_image_data = await upload_profile_image(file)
        image_public_id = profile_image_data["uuid"]
        profile_image_path = profile_image_data["secure_url"]
        
   
    else:

        if gender is None:
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/default_wjormw.png"
        elif gender.lower() == "male":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794267/male_fu4acn.jpg"
        elif gender.lower() == "female":
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/female_rwr0am.jpg"
        else:
            profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/default_wjormw.png"
        image_public_id = None
    profileImage= profile_image_path
   
    createProfile = ProfileTable(
        userId=user_data.id,
        name=name,
        gender=gender,
        profileImage=profileImage,
        image_public_id=image_public_id,
        dateOfBirth=dateOfBirth,
        designation=designation,
        companyName=companyName,
        createdOn=user.createdOn
    )

    db.add(createProfile)
    db.commit()
    db.refresh(createProfile)

    return {"message": "Profile created successfully", "profile": createProfile}



@router.put("/update-profile/")
async def update_profile(
    name: Optional[str] = Form(None),
    gender: Optional[GenderEnum]=Form(default=None, example=None),
    dateOfBirth: Optional[date] = Form(default=None, example=None),
    designation: Optional[str] = Form(default=None, example=None),
    companyName: Optional[str] = Form(default=None, example=None),
    file: Optional[UploadFile] = File(default=None, example=None),  
    remove :Optional[bool] =False, 
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
):
    if gender == "":
       gender = None
    if dateOfBirth == "":
       dateOfBirth = None
    if designation == "":
       designation = None   
    if companyName == "":
       companyName = None


    if dateOfBirth is not None:
       try:
           dateOfBirth_valid = validate_dob(dateOfBirth)
       except ValueError as e:
           raise HTTPException(status_code=422, detail=str("invalid dateOfBirth: " + str(e)))
    profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
    if not profile:
        return {"error": "Profile not found"}
    
    
      
    
    if file:
        profile_image_data = await upload_profile_image(file)
        image_public_id = profile_image_data["uuid"]
        profile_image_path = profile_image_data["secure_url"]
    
    elif remove:
        if profile.image_public_id:
            delete_profile_image(profile.image_public_id)

            g = gender 
            if g.lower() == "male":
               profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794267/male_fu4acn.jpg"
               image_public_id = None
            elif g.lower() == "female":
               profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/female_rwr0am.jpg"
               image_public_id = None
            else:
               profile_image_path = "https://res.cloudinary.com/ds7itk6lz/image/upload/v1765794159/default_wjormw.png"
               image_public_id = None
        else :
            return {"error": "No profile image to remove."}        
    else :
            profile_image_path = profile.profileImageUrl
            image_public_id = profile.image_public_id

    profile.name = name or profile.name
    profile.gender = gender or profile.gender
    profile.dateOfBirth = dateOfBirth or profile.dateOfBirth
    profile.designation = designation or profile.designation
    profile.companyName = companyName or profile.companyName
    profile.profileImageUrl = profile_image_path
    profile.image_public_id = image_public_id
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "profile": {
            "userId": profile.userId,
            "name": profile.name,
            "gender": profile.gender,
            "dateOfBirth": profile.dateOfBirth ,
            "designation": profile.designation,
            "companyName": profile.companyName,
            "profileImage": profile.profileImage,
            "profile_image_public_id": profile.image_public_id,
            "createdOn": profile.createdOn,
            "updatedOn": profile.updatedOn
        }
    }


# @router.get("/")
# def get_profile(request: Request, db: Session = Depends(get_db),user_data: dict = Depends(get_current_user)  ):
#     profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
   
#     if not profile:
#         return {"error": "Profile not found"}

#     profile_image_url = profile.profileImage


#     return {
#         "profile": {
#             "userId": profile.userId,
#             "name": profile.name,
#             "email": profile.email,
#             "phone": profile.phone,
#             "gender": profile.gender,
#             "dateOfBirth": profile.dateOfBirth,
#             "designation": profile.designation,
#             "companyName": profile.companyName,
#             "profileImage": profile_image_url,
#             "createdOn": profile.createdOn,
#             "updatedOn": profile.updatedOn
#         }
#     }


@router.get("/")
def get_profile(request: Request, db: Session = Depends(get_db),user_data: dict = Depends(get_current_user)  ):
    profile = db.query(ProfileTable).filter(ProfileTable.userId == user_data.id).first()
    if not profile:
        return {"error": "Profile not found"}
       
    


    return {
        "profile": {
            "userId": profile.userId,
            "name": profile.name,
            "email": User.email,
            "phone": User.phone,
            "gender": profile.gender,
            "dateOfBirth": profile.dateOfBirth,
            "designation": profile.designation,
            "companyName": profile.companyName,
            "profileImage": profile.profileImage,
            "profile_image_public_id": profile.image_public_id,
            "createdOn": profile.createdOn,
            "updatedOn": profile.updatedOn
        }
    }