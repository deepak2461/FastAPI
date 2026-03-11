

import datetime
from uuid import uuid4

from sqlalchemy import Column, String , Integer, DateTime, ForeignKey 
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import ARRAY

from db import Base


import enums


class Tasks(Base):
    __tablename__ = 'tasks'
    title = Column(String)
    priority: enums.PriorityLevel = Column(String)
    description = Column(String)
    status: enums.Status = Column(String) 
    deadline = Column(DateTime, nullable=True)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True )
    uid = Column(String, default=lambda: str(uuid4())) 
    assigned_on = Column(DateTime, default=datetime.datetime.now)
    #assignee_id = Column(Integer, ForeignKey("users.id"), nullable=False, default="0")
    assignee_uname = Column(String, ForeignKey("users.username"), nullable=False, default = "POOL_0")
    assignee = Relationship("User", back_populates="tasks")

    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # SELECT setval('users_id_seq', (SELECT MAX(id) FROM users)); 
    name = Column(String)
    username = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)
    Address = Column(String, nullable=True)
    Assigned_task_ids = Column(ARRAY(Integer), nullable=True)   # or use    Column(JSONB)
    tasks = Relationship("Tasks", back_populates="assignee")

