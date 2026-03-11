from pydantic import BaseModel, Field , field_validator
from typing import Optional
from datetime import datetime 
from uuid import uuid4

from enums import PriorityLevel, Status

#Pydantic models for request and response bodies

# Task related pydantic models
class TaskBase(BaseModel):
    title: str
    priority: PriorityLevel
    description : Optional[str] = None
    status: Status
    deadline: Optional[datetime] = None
    #assignee_uname  : Optional[str] = "POOL_0"

    @field_validator("deadline")
    def validate_deadline(cls, deadline):
        if deadline is not None and deadline.replace(tzinfo=None) < datetime.now():
            raise ValueError("Deadline must be a future date")
        return deadline
    

class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    #id: int = Field(default_factory=lambda: len(task_list), description="ID for the task")
    id : int 
    uid: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the task")
    assigned_on: datetime = Field(default_factory=datetime.now, description="Date when the task was assigned")
    assignee_uname : Optional[str] = Field(default="POOL_0", description="User to whom the task is assigned")
    

class Taskviewer(BaseModel):
    data: list[Task]
    message: str

class OneTaskViewer(BaseModel):
    data: Task
    message: str

class TaskUpdate(BaseModel):
    priority: Optional[PriorityLevel] = None
    description : Optional[str] = None
    status: Optional[Status] = None
    deadline: Optional[datetime] = None


# Users related pydantic models

class UserCreate(BaseModel):
    name: str
    age: int
    gender: str
    Address: Optional[str] = None

    @field_validator("age")
    def validate_age(cls, value):
        if value < 0:
            raise ValueError("Age must be a positive integer")
        return value
    
    model_config = {                # It tells Pydantic: If input is an object, read its attributes instead of expecting dict.
        "from_attributes": True     # This configuration allows Pydantic to create a User model instance from an instance of the db_models.User class, which is useful when retrieving user data from the database and returning it in the API response.
    }



class User(UserCreate):
    id: int             #= Field(default_factory=lambda: len(users)+1, description="ID for the user")
    username: str
    Assigned_task_ids : Optional[list[int]] = None  
 

class Users(BaseModel):
    data: list[User]
    message: str

