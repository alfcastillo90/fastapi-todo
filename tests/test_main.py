import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="module")
async def async_client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@app.dependency_overrides[get_db] = db_session

@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post("/tasks/", json={"text": "Test Task", "completed": False})
    assert response.status_code == 200
    assert response.json()["text"] == "Test Task"
    assert response.json()["completed"] is False

@pytest.mark.asyncio
async def test_read_tasks(async_client):
    response = await async_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_update_task(async_client):
    response = await async_client.post("/tasks/", json={"text": "Task to Update", "completed": False})
    task_id = response.json()["id"]
    response = await async_client.put(f"/tasks/{task_id}", json={"text": "Updated Task", "completed": True})
    assert response.status_code == 200
    assert response.json()["text"] == "Updated Task"
    assert response.json()["completed"] is True

@pytest.mark.asyncio
async def test_delete_task(async_client):
    response = await async_client.post("/tasks/", json={"text": "Task to Delete", "completed": False})
    task_id = response.json()["id"]
    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
