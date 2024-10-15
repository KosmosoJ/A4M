from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import find_dotenv, load_dotenv
from os import getenv


if find_dotenv():
    load_dotenv()
else:
    exit()

DB_PATH = getenv("DB")


engine = create_async_engine(url=DB_PATH, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
