from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: Task):
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def update_task(db: AsyncSession, task_id: int, title: str, description: str, score: int, completed: bool):
    task = await db.get(Task, task_id)
    if task:
        task.title = title
        task.description = description
        task.score = score
        task.completed = completed
        await db.commit()
        await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int):
    task = await db.get(Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
    return task
