# api/db.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_URL = os.getenv("URL")
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
