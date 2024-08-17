from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from database import Base

class BaseEntity(Base):
    __abstract__ = True   # 해당 클래스가 테이블로 생성되지 않도록 설정

    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

class Board(BaseEntity):
    __tablename__ = "board"

    id = Column(Integer, primary_key = True, autoincrement = True)
    member_id = Column(Integer, ForeignKey("member.id"))
    title = Column(String(255), nullable = False)
    content = Column(String(1000), nullable = False)

class Member(BaseEntity):
    __tablename__ = "member"

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String(255), nullable = False)
    name = Column(String(255), nullable = False)