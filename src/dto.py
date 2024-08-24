from datetime import datetime
from typing import List
from pydantic import BaseModel

class CreateBoardRequest(BaseModel):
    title: str
    content: str

class UpdateBoardRequest(BaseModel):
    title: str
    content: str


class member_create(BaseModel):
    email: str
    password: str
    name: str

class member_data(BaseModel):
    email: str
    name: str
    point: int
    isreviewer: bool

class room_create_list(BaseModel):
    sender_id: int
    title: str
    receiver_id_list: List[int]
    message: str
    item_id: int

class room_create(BaseModel):
    sender_id: int
    title: str
    receiver_id: int
    message: str
    item_id: int

class room_data(BaseModel):
    id: int
    title: str
    sender_id: int
    receiver_id: int
    updated_at: datetime
    isaccepted: bool
    item_id: int

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
            "isaccepted": self.isaccepted,
            "item_id": self.item_id
        }
    
class chat_message_create(BaseModel):
    room_id: int
    sender_id: int
    content: str

class chat_message_data(BaseModel):
    id: int
    room_id: int
    sender_id: int
    content: str
    created_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "member_id": self.sender_id,
            "content": self.content,
            "created_at_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }