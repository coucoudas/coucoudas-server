from fastapi import FastAPI

from src.api.board_api import board_router

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

app.include_router(board_router, prefix = "/api")