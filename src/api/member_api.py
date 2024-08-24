from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.service import MemberService
from src.dto import *

from src.database import connect_database

member_router = APIRouter(
    prefix = "/members",
    tags = ["member"]
)

@member_router.post("")
def create_member(request: Request, member_create: member_create):
    member = MemberService.create_member(member_create)
    return JSONResponse(
        status_code = 201, 
        content = {
            "message": "created"
        }
    )

@member_router.get("/{id}")
def find_member_by_id(request: Request, id: int):
    member = MemberService.find_member_by_id(id)
    member = MemberService.to_dict(member)
    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success",
            "results": member
        }
    )

@member_router.get("/reviewers/{id}")
def get_is_reviewer(id: int):
    member = MemberService.find_member_by_id(id)
    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success",
            "results": member.isreviewer
        }
    )

@member_router.put("/reviewers/{id}")
def switch_isreviewer(id: int):
    if MemberService.switch_isreviewer(id):
        return JSONResponse(
            status_code = 200, 
            content = {
                "message": "success"
            }
        )
    else:
        return JSONResponse(
            status_code = 404, 
            content = {
                "message": "not found"
            }
        )