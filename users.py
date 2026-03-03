from ast import Add
from fastapi import APIRouter

from pydantic import BaseModel, Field , field_validator
from typing import Optional

from datetime import datetime




#routers for user-related endpoints

router = APIRouter()

class User(BaseModel):
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
def get_user():
    return Users(data=users, message="success")

@router.post("/users")
def create_user(user: User):
    users.append(user.model_dump())
    return {"data": user, "message": "user created successfully"}