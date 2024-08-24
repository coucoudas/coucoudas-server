from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import connect_database
from src.gpt_ai import detect_private_information

gpt_router = APIRouter(
    prefix = "/gpt",
    tags = ["GPT"]
)

@gpt_router.get(path = "/abusing")
def get_response(message: str):
    test_message = "아 그 물건 진짜 마음에 드는데 제 전화번호 드릴테니까 혹시 연락주실 수 있나요? 제 전화번호는 01022293461입니다"
    result = detect_private_information(test_message)
    return { "status": 200, "message": result }