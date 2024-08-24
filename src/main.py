from fastapi import FastAPI

from src.api.board_api import board_router

app = FastAPI(
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json",
    redoc_url=None
)

app.include_router(board_router, prefix = "/api")