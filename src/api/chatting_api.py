import random
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service import ChatService
from src.entity import Room
from src.dto import chat_message_create, room_create, room_create_list
from src.database import connect_database

chat_router = APIRouter(
    prefix = "/chat",
    tags = ["chatting"]
)

@chat_router.post("/rooms")
def create_room(room: room_create_list):
    receiver_id_list = room.receiver_id_list
    if len(receiver_id_list) > 3:
        receiver_id = random.sample(receiver_id_list, 3)
    else:
        receiver_id = receiver_id_list
    created_room = []

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

    return JSONResponse(
        status_code = 201,
        content = {
            "message": "success"
        }
    )

# TODO: 거절 API
@chat_router.delete("/rooms/{room_id}")
def deny_chat_request(room_id: int):
    pass

# 수락 시 나머지 채팅방 확인 후 삭제
@chat_router.put("/rooms")
def accept_room(room_id: int):
    ChatService.accept_room(room_id)

    return JSONResponse(
        status_code = 201,
        content = {
            "message": "success"
        }
    )

# 내 방 리스트
@chat_router.get("/rooms")
def room_list(user_id: int):
    rooms = ChatService.get_room_list(user_id)

    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success",
            "results": [room.to_dict() for room in rooms]
        }
    )

@chat_router.post("/rooms/chat")
def chat_message(chat: chat_message_create):
    if ChatService.create_chat_message(chat) == False:
        return JSONResponse(
            status_code = 400,
            content = {
                "message": "fail"
            }
        )
    return {"message": "success"}

@chat_router.get("/rooms/chat/{room_id}")
def chat_message_list(room_id: int):
    chat_messages = ChatService.get_chat_message_list(room_id)

    return JSONResponse(
        status_code = 200,
        content = {
            "message": "success",
            "results": [chat.to_dict() for chat in chat_messages]
        }
    )

@chat_router.delete("/rooms/chat/{room_id}")
def delete_chat_message(room_id: int):
    ChatService.delete_chat_message(room_id)

    return JSONResponse(
        status_code = 201,
        content = {
            "message": "success"

        }
    )
# 리뷰어에 대한 추천
@chat_router.put("/rooms/like/{room_id}")
def like_room_reviewer(room_id: int):
    ChatService.add_like(room_id)

    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success"
        }
    )

# 리뷰어에 대한 비추천
@chat_router.put("/rooms/dislike/{room_id}")
def dislike_room_reviewer(room_id: int):
    ChatService.add_dislike(room_id)

    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success"
        }
    )

# 해당 유저의 추천 개수 반환
@chat_router.get("/rooms/recommandations/{user_id}")
def get_recommand_counts(user_id: int):
    result = ChatService.find_recommand_counts(user_id)

    return JSONResponse(
        status_code = 200, 
        content = {
            "message": "success",
            "results": result
        }
    )

@chat_router.get("/rooms/list")
def get_room_list(user_id: int):
    rooms = ChatService.get_last_messages_for_user(user_id)
    print(rooms)
    return JSONResponse(
        status_code = 200,
        content = {
            "message": "success",
            "results": rooms
        }
    )

#accept되지 않은 경우 대화 불가능 하게 막을 것