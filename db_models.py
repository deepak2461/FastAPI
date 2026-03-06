

import datetime
from uuid import uuid4

from sqlalchemy import Column, String , Integer, DateTime


from db import Base
from tasks import PriorityLevel, Status




class task_list(Base):
    __tablename__ = 'task_list'
    title = Column(String)
    priority:PriorityLevel = Column(String)
    description = Column(String)
    status: Status = Column(String) 
    deadline = Column(DateTime, nullable=True)
    assignee = Column(String, nullable=True, default="POOL")
    id = Column(Integer, primary_key=True, autoincrement=True, index=True )
    uid = Column(String, default=lambda: str(uuid4())) 
    assigned_on = Column(DateTime, default=datetime.datetime.now)
    

class User(Base):
    __tablename__ = 'users_temp'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # SELECT setval('users_id_seq', (SELECT MAX(id) FROM users)); 
    name = Column(String)
    username = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)
    Address = Column(String, nullable=True)

