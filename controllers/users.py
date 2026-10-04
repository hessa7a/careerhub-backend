# controllers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import UserModel
from serializers.user import (
    UserSchema,
    UserRegistrationSchema,
    UserLoginSchema,
    UserTokenSchema
)
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserTokenSchema, status_code=201)
def create_user(user: UserRegistrationSchema, db: Session = Depends(get_db)):

    # Check if the email already exists
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Create the new user
    new_user = UserModel(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role
    )

    # Hash the password before saving it
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = new_user.generate_token()

    return {
        "token": token,
        "message": "Login successful"
    }


@router.post("/login", response_model=UserTokenSchema, status_code=201)
def login(user: UserLoginSchema, db: Session = Depends(get_db)):

    # Find the user by email
    db_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    # Check if the user exists and password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(
            status_code=409,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = db_user.generate_token()

    return {
        "token": token,
        "message": "Login successful"
    }


@router.get("/current_user", response_model=UserSchema)
def current_user(user: UserSchema = Depends(get_current_user)):
    return user