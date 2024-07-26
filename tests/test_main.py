import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.database.database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield ac
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_task(client):
    response = await client.post("/tasks/", json={"title": "Test Task", "description": "Test Description", "score": 1, "completed": False})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

@pytest.mark.asyncio
async def test_read_tasks(client):
    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_task(client):
    response = await client.post("/tasks/", json={"title": "Test Task", "description": "Test Description", "score": 1, "completed": False})
    task_id = response.json()["id"]
    response = await client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description", "score": 5, "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

@pytest.mark.asyncio
async def test_delete_task(client):
    response = await client.post("/tasks/", json={"title": "Test Task", "description": "Test Description", "score": 1, "completed": False})
    task_id = response.json()["id"]
    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
