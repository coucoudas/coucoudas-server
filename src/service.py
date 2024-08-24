from .entity import *
from .database import connect_database
from .dto import *
from .gpt_ai import detect_private_information

from sqlalchemy import desc, or_, func

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
            isaccepted = room.isaccepted,
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

    def add_like(room_id: int):
        with connect_database() as database:
            room = database.query(Room).filter(
                Room.id == room_id,
            ).first()

            room.like = True

            database.commit()
            database.refresh(room)
        
    def add_dislike(room_id: int):
        with connect_database() as database:
            room = database.query(Room).filter(
                Room.id == room_id,
            ).first()

            room.dislike = True

            database.commit()
            database.refresh(room)

    def find_recommand_counts(user_id: int):
        with connect_database() as database:
            result = database.query(func.sum(Room.like)).filter(
                Room.receiver_id == user_id,
                Room.is_deleted == False,
                Room.like == True
            ).scalar()
        
    def find_by_room_id(room_id: int):
        with connect_database() as database:
            room = database.query(Room).filter(Room.id == room_id).first()
            return ChatService.to_room_data(room)
        

    def to_chat_message_data(chat_message: ChatMessage):
        return chat_message_data(
            id = chat_message.id,
            room_id = chat_message.room_id,
            sender_id = chat_message.sender_id,
            content = chat_message.content,
            created_at = chat_message.created_at
        )

    def to_chat_message_db(chat_message_create: chat_message_create):
        return ChatMessage(
            room_id = chat_message_create.room_id,
            sender_id = chat_message_create.sender_id,
            content = chat_message_create.content
        )

    def create_chat_message(chat: chat_message_create):
        gpt_content = detect_private_information(chat.content)
        
        with connect_database() as database:
            room = ChatService.find_by_room_id(chat.room_id).isaccepted
            if room and room == False:
                return False

            chat_message = ChatMessage(
                room_id = chat.room_id,
                sender_id = chat.sender_id,
                content = gpt_content
            )
            database.add(chat_message)
            database.commit()
            database.refresh(chat_message)
        return True
    
    def get_chat_message_list(room_id: int):
        with connect_database() as database:
            chat_messages = database.query(ChatMessage).filter(ChatMessage.room_id == room_id).all()
            return [ChatService.to_chat_message_data(chat_message) for chat_message in chat_messages]
        

    def delete_chat_message(room_id: int):
        with connect_database() as database:
            chat_messages = database.query(Room).filter(Room.id == room_id).first()
            database.delete(chat_messages)
            database.commit()
        return True
    
    def get_last_messages_for_user(user_id: int):
        # 유저가 참여한 모든 방을 가져옵니다.
        with connect_database() as database:
            rooms = database.query(Room).filter(
                (Room.sender_id == user_id) | (Room.receiver_id == user_id)
            ).all()

            room_messages = []

            for room in rooms:
                # 각 방에서 가장 마지막 채팅 내역을 가져옵니다.
                last_message = database.query(ChatMessage).filter(
                    ChatMessage.room_id == room.id
                ).order_by(desc(ChatMessage.created_at)).first()

                room_info = {
                    "room_id": room.id,
                    "sender_id": room.sender_id,
                    "receiver_id": room.receiver_id,
                    "content": last_message.content if last_message else None
                }

                room_messages.append(room_info)

            return room_messages