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

@member_router.post("/create")
def create_member(request: Request, member_create: member_create):
    member = MemberService.create_member(member_create)
    return JSONResponse(status_code = 200, content = {"message": "success"})

@member_router.get("/find/{id}")
def find_member_by_id(request: Request, id: int):
    member = MemberService.find_member_by_id(id)
    member = MemberService.to_dict(member)
    return JSONResponse(status_code = 200, content = member)

@member_router.get("/get/isreviewer/{id}")
def get_isreviewer(id: int):
    member = MemberService.find_member_by_id(id)
    return JSONResponse(status_code = 200, content = {"isreviewer": member.isreviewer})

@member_router.get("/switch/isreviewer/{id}")
def switch_isreviewer(id: int):
    if MemberService.switch_isreviewer(id):
        return JSONResponse(status_code = 200, content = {"message": "success"})
    else:
        return JSONResponse(status_code = 400, content = {"message": "fail"})
    
@member_router.get("/get/point/{id}")
def get_point(id: int):
    member = MemberService.find_member_by_id(id)
    return JSONResponse(status_code = 200, content = {"point": member.point})

@member_router.get("/point_plus")
def point_plus(id: int, amount: int=0):
    if MemberService.point_plus(id, amount):
        return JSONResponse(status_code = 200, content = {"message": "success"})
    else:
        return JSONResponse(status_code = 400, content = {"message": "fail"})
    
@member_router.get("/point_minus")
def point_minus(id: int, amount: int=0):
    if MemberService.point_minus(id, amount):
        return JSONResponse(status_code = 200, content = {"message": "success"})
    else:
        return JSONResponse(status_code = 400, content = {"message": "fail"})
