from fastapi import FastAPI

from src.api.route import root_router
from src.api.board.route import board_router

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


app.include_router(root_router, prefix="/api")
app.include_router(board_router, prefix = "/api") 