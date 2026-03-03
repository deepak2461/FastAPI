from ast import Add
from fastapi import APIRouter, Depends

from pydantic import BaseModel, Field , field_validator
from typing import Optional

from datetime import datetime


from db_conf import get_db
import db_models

from sqlalchemy.orm import Session


#routers for user-related endpoints

router = APIRouter()

class User(BaseModel):
    id : int = Field(default_factory=lambda: len(users)+1, description="ID for the user")
    name: str
    age: int
    gender: str= Field(description="Gender of the user")
    Address: Optional[str] = Field(default=None, description="Address of the user")

    @field_validator("age")
    def validate_age(cls, value):
        if value < 0:
            raise ValueError("Age must be a positive integer")
        return value

class Users(BaseModel):
    data: list[User]
    message: str



users = []

@router.get("/users", response_model=Users)
def get_user(db: Session = Depends(get_db)):
    users = db.query(db_models.User).all()
    #users = [User(id=user.id, name=user.name, age=user.age, gender=user.gender, Address=user.Address) for user in db_users]
    return Users(data=users, message="success")

@router.post("/users")
def create_user(user: User , db: Session = Depends(get_db)):
    # users.append(user.model_dump())
    # return {"data": user, "message": "user created successfully"}

    # users = db_models.User(
    #     name=user.name,
    #     age=user.age,
    #     gender=user.gender,
    #     Address=user.Address
    # )
    users = db_models.User(**user.model_dump()) # As model_dump() returns a dictionary of the model's data, we can unpack it using ** to create an instance of db_models.User with the same attributes as the User model.
    db.add(users)
    db.commit()
    db.refresh(users)
    return {"data": users, "message": "user created successfully"}


