from sqlalchemy.orm import Session

from .entity import Board
from .dto import CreateBoardRequest, UpdateBoardRequest

def insert_board(board_request: CreateBoardRequest, db: Session):
    board = Board(
        title = board_request.title,
        content = board_request.content
    )

    db.add(board)
    db.commit()

    return board.id

def find_boards(db: Session):
    results = db.query(Board).filter(Board.is_deleted == False).all()
    return results

def find_board(id: int, db: Session):
    result = db.query(Board).filter(Board.id == id).first()
    return result

def update_board(
    id: int,
    board_request: UpdateBoardRequest,
    db: Session
):
    result = find_board(id, db)

    result.title = board_request.title
    result.content = board_request.content

    db.commit()
    db.refresh(result)


