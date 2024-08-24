from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.dto import CreateBoardRequest, UpdateBoardRequest
from src.database import connect_database
from src.model import insert_board, find_boards, find_board, update_board, delete_board

chat_router = APIRouter(
    prefix = "/chat",
    tags = ["chatting"]
)