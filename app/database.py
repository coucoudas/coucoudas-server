from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

database_engine = create_engine(
    database_url, 
    pool_size = 10, 
    echo = True, 
    connect_args = { "check_same_thread": False }
)

Base = declarative_base()

def create_database():
    database = SessionLocal()
    
    try:
        yield database
    finally:
        database.close()
