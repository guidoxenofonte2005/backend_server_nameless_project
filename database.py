import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine)


class BaseModel(DeclarativeBase):
    pass


async def load_database():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()
