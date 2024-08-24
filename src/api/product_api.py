from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import connect_database

product_router = APIRouter(
    prefix = "/products",
    tags = ["product"]
)