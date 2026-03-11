from ast import Add
from fastapi import APIRouter, Depends

from db_conf import get_db
import db_models

from sqlalchemy.orm import Session

from py_models import UserCreate, Users

#routers for user-related endpoints

router = APIRouter()



#users = []

@router.get("/users", response_model=Users)
def get_user(db: Session = Depends(get_db)):
    users = db.query(db_models.User).order_by(db_models.User.id).all()  # This line retrieves all user records from the database, orders them by their ID, and returns the result as a list of db_models.User instances. The .all() method is called twice to first execute the query and then to retrieve the results as a list.
    print(users)
    for user in users:
        print(user.__dict__)
    count_of_users = db.query(db_models.User).count()
    #return Users(data=users, message="success")  # Added model_config in User pydantic class. Error :  Input should be a valid dictionary or instance of User [type=model_type, input_value=<db_models.User object at 0x0000011428169D90>, input_type=User] For further information visit https://errors.pydantic.dev/2.12/v/model_type
    return {"data": users, "message": f"success -- Retrieved {count_of_users} users"}

@router.post("/users")
def create_user(user: UserCreate , db: Session = Depends(get_db)):
    users = db_models.User(**user.model_dump()) # As model_dump() returns a dictionary of the pydantic model's data, we can unpack it using ** to create an instance of db_models.User with the same attributes as the User model.
    db.add(users)
    db.commit()
    db.refresh(users)

    users.username = f"{users.name}_{users.id}"
    db.commit()
    db.refresh(users)
    return {"data": users, "message": f"user with id {users.id} and username {users.username} created successfully"}


