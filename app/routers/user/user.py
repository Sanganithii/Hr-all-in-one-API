from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session    
from app.common.model import User
from app.common.database_conn import get_db   
from app.schemas.user import UserCreate
import logging   
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.utils.jwt_handler import create_access_token    
from app.utils.security import get_current_user                 


logger = logging.getLogger()

router = APIRouter()

@router.post("/register",)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = User(**data.model_dump(exclude_unset=True))

    new_user.set_password(data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    logger.info(f"New user registered: {new_user.email}")

    return {"message": "User registered successfully", "user_id": new_user.id}



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Accept username as email or phone
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.phone == form_data.username)
    ).first()
    # if not form_data.email and not form_data.phone:
    #     raise HTTPException(status_code=400, detail="Either email or phone must be provided.")
    # if form_data.email:
    #     user = db.query(User).filter(User.email == form_data.email).first()
    # else:
    #     user = db.query(User).filter(User.phone == form_data.phone).first()
    

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token({"user_id": user.id})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }



@router.put("/users/update")
def update_user(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated = False

    
    if data.email is not None:
        if data.email != current_user.email:
            exists = db.query(User).filter(User.email == data.email).first()
            if exists:
                raise HTTPException(400, "Email already exists")
            current_user.email = data.email
            updated = True

    if data.phone is not None:
        current_user.phone = data.phone
        updated = True


    if data.old_password is not None and data.new_password is None:
        raise HTTPException(
            status_code=400,
            detail="Enter new password"
        )

    if data.new_password is not None and data.old_password is None:
        raise HTTPException(
            status_code=400,
            detail="Enter old password is required"
        )

    if data.old_password is not None and data.new_password is not None:
        if not current_user.verify_password(data.old_password):
            raise HTTPException(
                status_code=400,
                detail="Old password is incorrect"
            )

        current_user.set_password(data.new_password)
        updated = True

    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No valid fields for update"
        )

    db.commit()
    db.refresh(current_user)

    return {"message": "User updated successfully"}




@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "phone": current_user.phone
    }