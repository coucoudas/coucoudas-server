from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dto import CreateBoardRequest, UpdateBoardRequest
from src.database import connect_database
from src.model import insert_board, find_boards, find_board, update_board, delete_board

board_router = APIRouter(
    prefix = "/boards",
    tags = ["board"]
)

# Create Board
@board_router.post(path = "", description = "게시판 생성 API")
def create_board(
    board_request: CreateBoardRequest, 
    db: Session = Depends(connect_database)
):
    result = insert_board(board_request, db)
    return { "status": 201, "message": f"/boards/{result}"}

# Read Board List
@board_router.get(path = "", description = "게시판 전체 조회 API")
def get_boards(db: Session = Depends(connect_database)):
    results = find_boards(db)
    return { "status": 200, "message": "SUCCESS", "data": results }

# Read Board
@board_router.get(path = "/{id}", description = "게시판 상세 조회 API")
def get_board(id: int, db: Session = Depends(connect_database)):
    result = find_board(id, db)
    return { "status": 200, "message": "SUCCESS", "data": result }

# Update Board
@board_router.patch(path = "/{id}", description = "게시판 수정 API")
def edit_board(
    id: int,
    board_request: UpdateBoardRequest,
    db: Session = Depends(connect_database)
):
    update_board(id, board_request, db)
    return { "status": 200, "message": "SUCCESS" }

# Delete Board
@board_router.delete(path = "/{id}", description = "게시판 삭제 API")
def remove_board(id: int, db: Session = Depends(connect_database)):
    delete_board(id, db)
    return { "status": 200, "message": "SUCCESS" }