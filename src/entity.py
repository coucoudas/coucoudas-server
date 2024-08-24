from sqlalchemy import TEXT, Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base, database_engine

class BaseEntity(Base):
    __abstract__ = True   # 해당 클래스가 테이블로 생성되지 않도록 설정

    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Board(BaseEntity):
    __tablename__ = "board"

    id = Column(Integer, primary_key = True, autoincrement = True)
    # member_id = Column(Integer, ForeignKey("member.id"))
    title = Column(String(255), nullable = False)
    content = Column(String(1000), nullable = False)

class Member(BaseEntity):
    __tablename__ = "member"

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String(255), nullable = False)
    name = Column(String(255), nullable = False)
    point = Column(Integer, default = 0)

class Room(BaseEntity):
    __tablename__ = "room"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(255), nullable = False)

class RoomMember(BaseEntity):
    __tablename__ = "room_member"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    room_id = Column(Integer, nullable = False)
    member_id = Column(Integer, nullable = False)

class ChatMessage(BaseEntity):
    __tablename__ = "room_chat_message"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    room_id = Column(Integer, nullable = False)
    member_id = Column(Integer, nullable = False)
    content = Column(String(255), nullable = False)

class Room(BaseEntity):
    __tablename__ = "room"

    id = Column(Integer, primary_key = True, autoincrement = True)
    topic = Column(TEXT, nullable = False)

class RoomUser(BaseEntity):
    __tablename__ = "room_user"

    id = Column(Integer, primary_key = True, autoincrement = True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    room = relationship("Room", back_populates="users")
    user = relationship("User", back_populates="rooms")

class RoomUserChat(BaseEntity):
    __tablename__ = "room_user_chat"

    id = Column(Integer, primary_key = True, autoincrement = True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    chat = Column(TEXT, nullable = False)
    room = relationship("Room", back_populates="chats")
    user = relationship("User", back_populates="chats")

Base.metadata.create_all(bind = database_engine)