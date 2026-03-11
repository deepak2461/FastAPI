from fastapi import APIRouter, Depends , HTTPException

from db_conf import get_db
import db_models

from sqlalchemy.orm import Session

from enums import PriorityLevel, Status
from py_models import TaskCreate, Taskviewer, OneTaskViewer, TaskUpdate


# Routers for task-related endpoints

trouter = APIRouter()

#task_list=[]
task_list = [
    {
      "title": "title1",
      "priority": "highh",
      "description": "desc1",
      "status": "completed",
      "deadline": "2026-04-21T10:18:46.091000Z",
      "id": 1,
      "uid": "43e5b9f2-ab91-4254-956a-8d4eb5ed78ad",
      "assigned_on": "2026-02-21T15:58:13.144994"
    },
    {
      "title": "title2",
      "priority": "highh",
      "description": "desc2",
      "status": "completed",
      "deadline": "2026-04-21T10:18:46.091000Z",
      "id": 2,
      "uid": "0f0a47c0-9dd0-4d18-848c-ac0a4c6b0f33",
      "assigned_on": "2026-02-21T15:58:14.501939"
    },
    {
      "title": "title3",
      "priority": "mediumm",
      "description": "desc3",
      "status": "in progress",
      "deadline": "2026-03-21T10:18:46.091000Z",
      "id": 3,
      "uid": "01f5bdd3-fa93-4dce-91ab-11cbee1ba85c",
      "assigned_on": "2026-02-21T15:58:30.629809"
    },
    {
      "title": "title4",
      "priority": "mediumm",
      "description": "desc4",
      "status": "in progress",
      "deadline": "2026-03-21T10:18:46.091000Z",
      "id": 4,
      "uid": "40dc1f08-87cd-4a31-9f15-c7425cb911e8",
      "assigned_on": "2026-02-21T15:58:39.217850",
      "assignee": "Deepak"
    },
    {
      "title": "title5",
      "priority": "loww",
      "description": "desc5",
      "status": "pending",
      "deadline": "2026-04-21T10:18:46.091000Z",
      "id": 5,
      "uid": "d1c8e7b9-9a0c-4f1b-8c3e-2a1f0e5b6c7d",
      "assigned_on": "2026-02-21T15:58:45.123456"
    }
  ]

@trouter.get("/view", response_model=Taskviewer, description="Get all tasks", summary="Gett tasks", tags=["tasks"])
def get_tasks(db: Session = Depends(get_db)):
    task_list = db.query(db_models.Tasks).order_by(db_models.Tasks.id).all()

    if not task_list:
        return {"data": task_list, "message": "No tasks found"}
    else:
        return {"data": task_list, "message": f"Retrieved {len(task_list)} tasks successfully"}


@trouter.post("/create", response_model=OneTaskViewer, description="Create a new task", summary="Createe task")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = task.model_dump()
    print(new_task)
    unpacked_new_task = db_models.Tasks(**new_task)
    print(unpacked_new_task)
    #unpacked_new_task = db_models.Tasks(**task.model_dump()) 
    db.add(unpacked_new_task)
    db.commit()
    db.refresh(unpacked_new_task)

    
    
    return {"data": unpacked_new_task, "message": f"Task with id -- {unpacked_new_task.id} created successfully"}


    
@trouter.get("/view/{task_id}", response_model=OneTaskViewer, description="Get a task by ID", summary="Get task by ID")
def get_task_by_id(task_id: int , db: Session = Depends(get_db)):
    task = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if task:
        return {"data": task, "message": f"Task with id {task_id} retrieved successfully"}
    else:
        raise HTTPException(status_code = 404, detail = f"Task with id {task_id} not found")


@trouter.get("/view/status/{task_status}", response_model=Taskviewer, description="Get tasks by status", summary="Get tasks by status")     #only works with /status/ in route
def get_tasks_by_status(task_status: Status , db: Session = Depends(get_db)):
    filtered_tasks = db.query(db_models.Tasks).filter(db_models.Tasks.status == task_status).all()
    if not filtered_tasks:
        return {"data": filtered_tasks, "message": f"No tasks found with status {task_status}"}
    else:
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks with status {task_status} successfully"}


    
@trouter.get("/view/priority/{task_priority}", response_model=Taskviewer, description="Get tasks by priority", summary="Get tasks by priority")
def get_tasks_by_priority(task_priority: PriorityLevel, db:Session = Depends(get_db)):
    filtered_tasks = db.query(db_models.Tasks).filter(db_models.Tasks.priority == task_priority).all()
    if not filtered_tasks:
        return {"data" : filtered_tasks, "message": f"No tasks found with priority {task_priority}"}
    else:
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks with priority {task_priority} successfully"}
    


@trouter.get("/view/assignee/{assignee_uname}", response_model=Taskviewer, description="Get tasks by assignee", summary="Get tasks by assignee")
def get_tasks_by_assignee(assignee_uname: str, db:Session = Depends(get_db)):
    filtered_tasks = db.query(db_models.Tasks).filter(db_models.Tasks.assignee_uname == assignee_uname).all()
    if not filtered_tasks:
        return {"data": filtered_tasks, "message" : f"No tasks found assigned to {assignee_uname}"}
    else :
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks assigned to {assignee_uname} successfully"}
    


    
@trouter.delete("/delete/{task_id}", description="Delete a task by ID", summary="Delete task by ID")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if deleted_task:
        db.delete(deleted_task)
        db.commit()
        db.refresh(deleted_task)
        return {"data": deleted_task, "message": f"Task with id {task_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")



@trouter.put("/update/{task_id}",response_model=OneTaskViewer, description="Update a task by ID", summary="Update task by ID")
def update_task(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task_db = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if not updated_task_db:
        raise HTTPException(status_code = 404, detail = f"Task with id {task_id} not found")
    else:
        updated_task_data = updated_task.model_dump(exclude_unset=True)
        for key, value in updated_task_data.items():
            setattr(updated_task_db, key, value)
        db.add(updated_task_db)
        db.commit()
        db.refresh(updated_task_db)
        return {"data" : updated_task_db, "message": f"Task with id {task_id} updated successfully"}
    

    # for index, task in enumerate(task_list):
    #     if task["id"] == task_id:
    #         task_list[index].update(updated_task.model_dump())
    #         return {"data": task_list[index], "message": f"Task with id {task_id} updated successfully"}
    # raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

@trouter.put("/assign/{task_id}", response_model=OneTaskViewer, description="Assign a task to a user", summary="Assign task to user")
def assign_task(task_id: int, assignee: str, db: Session = Depends(get_db)):
    updated_task_db = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if not updated_task_db:
        raise HTTPException(status_code = 404, detail = f"Task with id {task_id} not found")
    else:
        updated_task_db.assignee_uname = assignee
        db.add(updated_task_db)
        db.commit()
        db.refresh(updated_task_db)

        updated_user_db = db.query(db_models.User).filter(db_models.User.username == assignee).first()
        if updated_user_db:
                if updated_user_db.Assigned_task_ids is None:
                    updated_user_db.Assigned_task_ids = [updated_task_db.id]
                else:
                    print("Entered else in if")
                    print(f"Updated_task_db.id is {updated_task_db.id}")
                    #updated_user_db.Assigned_task_ids.append(updated_task_db.id)   # SQLAlchemy does NOT automatically detect in-place changes to mutable objects
                    updated_user_db.Assigned_task_ids = (updated_user_db.Assigned_task_ids + [updated_task_db.id])
                    print(f"Updated_user_db is {updated_user_db.Assigned_task_ids}")
                    fdata = db.query(db_models.User).all()
                    print(type(fdata))
                    print(fdata)
                    for user in fdata:
                        print(user.__dict__)
                db.add(updated_user_db)
                db.commit()
                db.refresh(updated_user_db)
        else:
            raise HTTPException(status_code = 404, detail = f"User with username {assignee} not found")
            


        return {"data" : updated_task_db, "message": f"Task with id {task_id} assigned to {assignee} successfully"}



    # for index, task in enumerate(task_list):
    #     if task["id"] == task_id:
    #         task_list[index]["assignee"] = assignee
    #         return {"data": task_list[index], "message": f"Task with id {task_id} assigned to {assignee} successfully"}
    # raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
