from fastapi import APIRouter, Depends, Response
from src.database import connect_database

root_router = APIRouter(
    tags = ["root"]
)

# Read Board List
@root_router.get(path = "/", description = "나는 주전자다",)
def get(response: Response):
    response.status_code = 418
    return "I'm a teapot"
