from fastapi import APIRouter , HTTPException

from pydantic import BaseModel, Field , field_validator
from typing import Optional

from datetime import datetime 
from enum import Enum
from uuid import uuid4







#Pydantic models for request and response bodies

class PriorityLevel(str, Enum):
    low = "loww"
    medium = "mediumm"
    high = "highh"

class Status(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: str
    priority:PriorityLevel
    description : Optional[str] = None
    status: Status
    deadline: Optional[datetime] = None
    assignee  : Optional[str] = "POOL"

    @field_validator("deadline")
    def validate_deadline(cls, deadline):
        if deadline is not None and deadline.replace(tzinfo=None) < datetime.now():
            raise ValueError("Deadline must be a future date")
        return deadline
    
    

class TaskCreate(TaskBase):
    pass


# class Task(BaseModel):
#     title: str
#     #Priority: str = Field(default={"low": 3, "medium": 2, "high": 1}, description="Priority levels for the task")
#     #priority: str = Field(default=None, description="Priority levels for the task", example="low", title="Task Priority")
#     priority: PriorityLevel = Field(description="Priority levels for the task", example="low", title="Task Priority")
#     description: Optional[str] = Field(default=None, description="Description of the Task")
#     #Status: str = Field(default=["pending", "in progress", "completed"], description="Status of the task")
#     #status : str = Field(description="Status of the task", example="pending", title="Task Status")
#     status: Status = Field(description="Status of the task", example="pending", title="Task Status")
#     Assigned_On: datetime= Field(default=datetime.now(), description="Date when the task was assigned")
#     Deadline : Optional[datetime] = Field(default=None, description="Deadline for the task")

class Task(TaskBase):
    #id: int = Field(default_factory=lambda: len(task_list), description="ID for the task")
    id : int 
    uid: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the task")
    assigned_on: datetime = Field(default_factory=datetime.now, description="Date when the task was assigned")
    assignee : Optional[str] = Field(default="POOL", description="User to whom the task is assigned")
    

class Taskviewer(BaseModel):
    data: list[Task]
    message: str

class OneTaskViewer(BaseModel):
    data: Task
    message: str




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
def get_tasks():
    if not task_list:
        return {"data": task_list, "message": "No tasks found"}
    else:
        return {"data": task_list, "message": f"Retrieved {len(task_list)} tasks successfully"}
# def get_tasks():
#     return {"data": task_list, "message": "Retrieved tasks successfully"}


#max_id = 0   
max_id = max(task["id"] for task in task_list) if task_list else 0
@trouter.post("/create", response_model=OneTaskViewer, description="Create a new task", summary="Createe task")
def create_task(task: TaskCreate):
    new_task = task.model_dump()
    #new_task["id"] = len(task_list) + 1
    global max_id
    max_id += 1
    new_task["id"] = max_id
    new_task["uid"] = str(uuid4())
    new_task["assigned_on"] = datetime.now()
    task_list.append(new_task)
    # task_list.append(task.model_dump())   
    print(task_list)
    # print("================================")
    # print(task_list[len(task_list)-1])
    #return {"data": task_list[len(task_list)-1], "message": "Task created successfully"}
    #return {"data": task_list, "message": "Task created successfully"}
    return {"data": new_task, "message": "Task created successfully"}
    
@trouter.get("/view/{task_id}", response_model=OneTaskViewer, description="Get a task by ID", summary="Get task by ID")
def get_task_by_id(task_id: int):
    for task in task_list:
        if task["id"] == task_id:
            return {"data": task, "message": f"Task with id {task_id} retrieved successfully"}
    # return {"data": None, "message": "Task not found"}
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

@trouter.get("/view/status/{task_status}", response_model=Taskviewer, description="Get tasks by status", summary="Get tasks by status")     #only works with /status/ in route
def get_tasks_by_status(task_status: Status):
    filtered_tasks = [task for task in task_list if task["status"] == task_status]
    if not filtered_tasks:
        return {"data": filtered_tasks, "message": f"No tasks found with status {task_status}"}
    else:
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks with status {task_status} successfully"}
    
@trouter.get("/view/priority/{task_priority}", response_model=Taskviewer, description="Get tasks by priority", summary="Get tasks by priority")
def get_tasks_by_priority(task_priority: PriorityLevel):
    filtered_tasks = [task for task in task_list if task["priority"] == task_priority]
    if not filtered_tasks:
        return {"data": filtered_tasks, "message": f"No tasks found with priority {task_priority}"}
    else:
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks with priority {task_priority} successfully"}

@trouter.get("/view/assignee/{assignee_name}", response_model=Taskviewer, description="Get tasks by assignee", summary="Get tasks by assignee")
def get_tasks_by_assignee(assignee_name: str):
    filtered_tasks = [task for task in task_list if task.get("assignee") == assignee_name] #CHECK THIS
    if not filtered_tasks:
        return {"data": filtered_tasks, "message": f"No tasks found assigned to {assignee_name}"}   
    else:
        return {"data": filtered_tasks, "message": f"Retrieved {len(filtered_tasks)} tasks assigned to {assignee_name} successfully"}


    
@trouter.delete("/delete/{task_id}", description="Delete a task by ID", summary="Delete task by ID")
def delete_task(task_id: int):
    for index, task in enumerate(task_list):
        if task["id"] == task_id:
            deleted_task = task_list.pop(index)
            return {"data": deleted_task, "message": f"Task with id {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

class TaskUpdate(BaseModel):
    priority: Optional[PriorityLevel] = None
    description : Optional[str] = None
    status: Optional[Status] = None
    deadline: Optional[datetime] = None

@trouter.put("/update/{task_id}",response_model=OneTaskViewer, description="Update a task by ID", summary="Update task by ID")
def update_task(task_id: int, updated_task: TaskUpdate):
    for index, task in enumerate(task_list):
        if task["id"] == task_id:
            task_list[index].update(updated_task.model_dump())
            return {"data": task_list[index], "message": f"Task with id {task_id} updated successfully"}
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

@trouter.put("/assign/{task_id}", response_model=OneTaskViewer, description="Assign a task to a user", summary="Assign task to user")
def assign_task(task_id: int, assignee: str):
    for index, task in enumerate(task_list):
        if task["id"] == task_id:
            task_list[index]["assignee"] = assignee
            return {"data": task_list[index], "message": f"Task with id {task_id} assigned to {assignee} successfully"}
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
