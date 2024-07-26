from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, get_db, init_db
from app import crud, schemas
from app.models import Task
from typing import List

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

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # URL del frontend de React
    "http://127.0.0.1:3000",  # Otra posible URL del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/tasks/", response_model=schemas.Task, tags=["tasks"])
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        score=task.score,
        completed=task.completed
    )
    return await crud.create_task(db, db_task)

@app.get("/tasks/", response_model=List[schemas.Task], tags=["tasks"])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db)

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["tasks"])
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db, task_id, task.title, task.description, task.score, task.completed)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task, tags=["tasks"])
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
