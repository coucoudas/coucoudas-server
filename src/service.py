from .entity import *
from .database import connect_database
from .dto import *
from sqlalchemy import or_

class MemberService:
    def to_member_db(member_create: member_create):
        return Member(
            email = member_create.email,
            password = member_create.password,
            name = member_create.name,
        )
    
    def to_member_data(member: Member):
        return member_data(
            email = member.email,
            name = member.name,
            point = member.point,
            isreviewer = member.isreviewer,
        )
    
    def create_member(member_create: member_create):
        with connect_database() as database:
            member = MemberService.to_member_db(member_create)
            database.add(member)
            database.commit()
            database.refresh(member)
        return True
    
    def find_member_by_id(id: int):
        with connect_database() as database:
            member = database.query(Member).filter(Member.id == id).first()
        return MemberService.to_member_data(member)
    
    def find_member_by_email(email: str):
        with connect_database() as database:
            member = database.query(Member).filter(Member.email == email).first()
        return MemberService.to_member_data(member)
    
    def to_dict(member: member_data):
        return {
            "email": member.email,
            "name": member.name,
            "point": member.point,
            "isreviewer": member.isreviewer,
        }
    def switch_isreviewer(id: int):
        with connect_database() as database:
            member = database.query(Member).filter(Member.id == id).first()
            member.isreviewer = not member.isreviewer
            database.commit()
        return True
    
    def point_plus(id: int, amount):
        with connect_database() as database:
            member = database.query(Member).filter(Member.id == id).first()
            member.point += amount
            database.commit()
        return True
    
    def point_minus(id: int, amount):
        with connect_database() as database:
            member = database.query(Member).filter(Member.id == id).first()
            if member.point < amount:
                return False
            member.point -= amount
            database.commit()
        return True
    

class ChatService:
    def to_room_db(room_create: room_create):
        return Room(
            title = room_create.title,
            sender_id = room_create.sender_id,
            receiver_id = room_create.receiver_id,
            item_id = room_create.item_id

        )
    
    def to_room_data(room: Room):
        return room_data(
            id = room.id,
            title = room.title,
            sender_id = room.sender_id,
            item_id = room.item_id,
            receiver_id = room.receiver_id,
            updated_at = room.updated_at
        )

    def create_room(room_create: room_create):
        with connect_database() as database:
            room = ChatService.to_room_db(room_create)
            database.add(room)
            database.commit()
            database.refresh(room)
        return room.id
    
    def accept_room(room_id: int):
        with connect_database() as database:
            room = database.query(Room).filter(Room.id == room_id).first()
            room.isaccepted = True
            database.commit()
            database.refresh(room)
            pair = set(room.pair)
            pair.remove(room_id)
            pair = list(pair)
            for pair_id in pair:
                database.delete(database.query(Room).filter(Room.id == pair_id).first())
            database.commit()

    def setpair(room_id, pair_room_id_list: List[int]):
        with connect_database() as database:
            room = database.query(Room).filter(Room.id == room_id).first()
            room.pair = pair_room_id_list
            database.commit()

    def get_room_list(id: int):
        with connect_database() as database:
            rooms = database.query(Room).filter(or_(Room.sender_id == id, Room.receiver_id == id)).all()
            return [ChatService.to_room_data(room) for room in rooms]
        
    