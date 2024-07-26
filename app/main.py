from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, get_db
from app import crud, schemas
from app.models import Task

app = FastAPI()

app = FastAPI(
    title="To-Do List API",
    description="API para gestionar una lista de tareas utilizando FastAPI y MySQL",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "tasks",
            "description": "Operaciones con tareas"
        }
    ]
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = Task(text=task.text, completed=task.completed)
    return await crud.create_task(db, db_task)

@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db, task_id, task.text, task.completed)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
