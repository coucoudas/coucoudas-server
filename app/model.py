from sqlalchemy.orm import Session

from .entity import Board
from .dto import CreateBoardRequest

def create_board(board_request: CreateBoardRequest, db: Session):
    board = Board(
        title = board_request.title,
        content = board_request.content
    )

    db.add(board)
    db.commit()

    return board.id