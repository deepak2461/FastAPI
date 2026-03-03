from fastapi import FastAPI



from pydantic import BaseModel, Field
from typing import Optional

from users import router as user_router
from tasks import trouter as task_router


app = FastAPI()

app.include_router(user_router, tags=["users"])
app.include_router(task_router, tags=["tasks"], prefix="/tasks")
