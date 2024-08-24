from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service import ChatService
from src.entity import Room
from src.dto import room_create, room_create_list
from src.database import connect_database

chat_router = APIRouter(
    prefix = "/chat",
    tags = ["chatting"]
)

@chat_router.post("/room/create")
def create_room(room: room_create_list):
    receiver_id = room.receiver_id_list
    created_room =  []
    for receiver in receiver_id:
        room_temp = room_create(
            sender_id = room.sender_id,
            title = room.title,
            receiver_id = receiver,
            message = room.message,
            item_id = room.item_id
        )
        made_room = ChatService.create_room(room_temp)
        created_room.append(made_room)
    for made_room in created_room:
        ChatService.setpair(made_room, created_room)
    return {"message": "success"}


@chat_router.get("/room/accept/{room_id}")
def accept_room(room_id: int):
    ChatService.accept_room(room_id)
    return {"message": "success"}

@chat_router.get("/room/list/{id}")
def room_list(id: int):
    room_list = ChatService.get_room_list(id)
    room_list = [room.to_dict() for room in room_list]
    return JSONResponse(status_code = 200, content = room_list)

