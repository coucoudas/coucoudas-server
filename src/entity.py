from sqlalchemy import JSON, Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .database import Base, database_engine

class BaseEntity(Base):
    __abstract__ = True   # 해당 클래스가 테이블로 생성되지 않도록 설정

    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Member(BaseEntity):
    __tablename__ = "member"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String(255), nullable = False)
    name = Column(String(255), nullable = False)
    point = Column(Integer, default = 0)
    isreviewer = Column(Boolean, default = False)

class Room(BaseEntity):
    __tablename__ = "room"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(255), nullable = False)
    sender_id = Column(Integer, nullable = False)
    receiver_id = Column(Integer, nullable = False)
    item_id = Column(Integer, nullable = False)
    isaccepted = Column(Boolean, default = False)
    pair = Column(JSON, nullable = True)
    room_chat_message = relationship("ChatMessage", cascade="all, delete")

class ChatMessage(BaseEntity):
    __tablename__ = "room_chat_message"
    __abstract__ = False

    id = Column(Integer, primary_key = True, autoincrement = True)
    room_id = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable = False)
    sender_id = Column(Integer, nullable = False)
    content = Column(String(255), nullable = False)

Base.metadata.create_all(bind = database_engine)