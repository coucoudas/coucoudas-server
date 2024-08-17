from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .dto import CreateBoardRequest
from .database import connect_database
from .model import create_board

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc')

# root page
@app.get("/")
def hello_world():
    return { "status": 200, "message": "hello" }

# Create Board
@app.post(path = "/boards", description = "게시판 생성 API")
def create_board_api(
    board_request: CreateBoardRequest, 
    db: Session = Depends(connect_database)
):
    result = create_board(board_request, db)
    return { "status": 201, "message": f"/boards/{result}"}