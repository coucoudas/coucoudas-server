from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .dto import CreateBoardRequest, UpdateBoardRequest
from .database import connect_database
from .model import insert_board, find_boards, find_board, update_board

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc')

# root page
@app.get("/")
def hello_world():
    return { "status": 200, "message": "hello world" }

# Create Board
@app.post(path = "/boards", description = "게시판 생성 API")
def create_board(
    board_request: CreateBoardRequest, 
    db: Session = Depends(connect_database)
):
    result = insert_board(board_request, db)
    return { "status": 201, "message": f"/boards/{result}"}

# Read Board List
@app.get(path = "/boards", description = "게시판 전체 조회 API")
def get_boards(db: Session = Depends(connect_database)):
    results = find_boards(db)
    return { "status": 200, "message": "SUCCESS", "data": results }

# Read Board
@app.get(path = "/boards/{id}", description = "게시판 상세 조회 API")
def get_board(id: int, db: Session = Depends(connect_database)):
    result = find_board(id, db)
    return { "status": 200, "message": "SUCCESS", "data": result }

# Update Board
@app.patch(path = "/boards/{id}", description = "게시판 수정 API")
def edit_board(
    id: int,
    board_request: UpdateBoardRequest,
    db: Session = Depends(connect_database)
):
    update_board(id, board_request, db)
    return { "status": 200, "message": "SUCCESS" }

# Delete Board