from enum import Enum


class PriorityLevel(str, Enum):
    low = "loww"
    medium = "mediumm"
    high = "highh"

class Status(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"


#  Tried for a dropdown while assigning a task to a user, but it is not working
# class BaseAvailUsers():
#     def get_users(db: Session = Depends(get_db)):
#         users = db.query(db_models.User).select(db_models.User.username).all()
#         return users
    
# class AvailableUsers(BaseAvailUsers):
#     userss = 

    