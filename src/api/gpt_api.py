from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import connect_database
from src.gpt_ai import get_gpt_response

gpt_router = APIRouter(
    prefix = "/gpt",
    tags = ["GPT"]
)

@gpt_router.get(path = "/abusing")
def get_response():
    result = get_gpt_response("hello")
    return { "status": 200, "message": result }