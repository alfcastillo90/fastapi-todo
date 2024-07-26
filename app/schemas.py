from pydantic import BaseModel

class TaskBase(BaseModel):
    text: str
    completed: bool

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
