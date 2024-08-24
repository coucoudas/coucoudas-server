from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import connect_database

gpt_router = APIRouter(
    prefix = "/gpt",
    tags = ["GPT"]
)