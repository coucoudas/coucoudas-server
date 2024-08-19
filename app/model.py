from sqlalchemy.orm import Session

from .entity import Board
from .dto import CreateBoardRequest

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