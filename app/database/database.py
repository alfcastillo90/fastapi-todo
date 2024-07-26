from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL
import pymysql
from urllib.parse import urlparse

# Parse the DATABASE_URL to extract connection parameters
url = urlparse(DATABASE_URL)
dbname = url.path[1:]  # Remove leading slash
user = url.username
password = url.password
host = url.hostname
port = url.port or 3306

# Create the database if it does not exist
connection = pymysql.connect(host=host, user=user, password=password, port=port)
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
cursor.close()
connection.close()

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session
