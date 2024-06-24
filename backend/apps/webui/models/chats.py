from pydantic import BaseModel, ConfigDict
from typing import List, Union, Optional

import json
import uuid
import time

from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import Session

from apps.webui.internal.db import Base, get_session


####################
# Chat DB Schema
####################


class Chat(Base):
    __tablename__ = "chat"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    title = Column(String)
    chat = Column(String)  # Save Chat JSON as Text

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    share_id = Column(String, unique=True, nullable=True)
    archived = Column(Boolean, default=False)


class ChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    chat: str

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch

    share_id: Optional[str] = None
    archived: bool = False


####################
# Forms
####################


class ChatForm(BaseModel):
    chat: dict


class ChatTitleForm(BaseModel):
    title: str


class ChatResponse(BaseModel):
    id: str
    user_id: str
    title: str
    chat: dict
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    share_id: Optional[str] = None  # id of the chat to be shared
    archived: bool


class ChatTitleIdResponse(BaseModel):
    id: str
    title: str
    updated_at: int
    created_at: int


class ChatTable:

    def insert_new_chat(self, user_id: str, form_data: ChatForm) -> Optional[ChatModel]:
        with get_session() as db:
            id = str(uuid.uuid4())
            chat = ChatModel(
                **{
                    "id": id,
                    "user_id": user_id,
                    "title": (
                        form_data.chat["title"]
                        if "title" in form_data.chat
                        else "New Chat"
                    ),
                    "chat": json.dumps(form_data.chat),
                    "created_at": int(time.time()),
                    "updated_at": int(time.time()),
                }
            )

            result = Chat(**chat.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            return ChatModel.model_validate(result) if result else None

    def update_chat_by_id(self, id: str, chat: dict) -> Optional[ChatModel]:
        with get_session() as db:
            try:
                chat_obj = db.get(Chat, id)
                chat_obj.chat = json.dumps(chat)
                chat_obj.title = chat["title"] if "title" in chat else "New Chat"
                chat_obj.updated_at = int(time.time())
                db.commit()
                db.refresh(chat_obj)

                return ChatModel.model_validate(chat_obj)
            except Exception as e:
                return None

    def insert_shared_chat_by_chat_id(self, chat_id: str) -> Optional[ChatModel]:
        with get_session() as db:
            # Get the existing chat to share
            chat = db.get(Chat, chat_id)
            # Check if the chat is already shared
            if chat.share_id:
                return self.get_chat_by_id_and_user_id(chat.share_id, "shared")
            # Create a new chat with the same data, but with a new ID
            shared_chat = ChatModel(
                **{
                    "id": str(uuid.uuid4()),
                    "user_id": f"shared-{chat_id}",
                    "title": chat.title,
                    "chat": chat.chat,
                    "created_at": chat.created_at,
                    "updated_at": int(time.time()),
                }
            )
            shared_result = Chat(**shared_chat.model_dump())
            db.add(shared_result)
            db.commit()
            db.refresh(shared_result)
            # Update the original chat with the share_id
            result = (
                db.query(Chat)
                .filter_by(id=chat_id)
                .update({"share_id": shared_chat.id})
            )

            return shared_chat if (shared_result and result) else None

    def update_shared_chat_by_chat_id(self, chat_id: str) -> Optional[ChatModel]:
        with get_session() as db:
            try:
                print("update_shared_chat_by_id")
                chat = db.get(Chat, chat_id)
                print(chat)
                chat.title = chat.title
                chat.chat = chat.chat
                db.commit()
                db.refresh(chat)

                return self.get_chat_by_id(chat.share_id)
            except:
                return None

    def delete_shared_chat_by_chat_id(self, chat_id: str) -> bool:
        try:
            with get_session() as db:
                db.query(Chat).filter_by(user_id=f"shared-{chat_id}").delete()
            return True
        except:
            return False

    def update_chat_share_id_by_id(
        self, id: str, share_id: Optional[str]
    ) -> Optional[ChatModel]:
        try:
            with get_session() as db:
                chat = db.get(Chat, id)
                chat.share_id = share_id
                db.commit()
                db.refresh(chat)
                return chat
        except:
            return None

    def toggle_chat_archive_by_id(self, id: str) -> Optional[ChatModel]:
        try:
            with get_session() as db:
                chat = self.get_chat_by_id(id)
                db.query(Chat).filter_by(id=id).update({"archived": not chat.archived})

                return self.get_chat_by_id(id)
        except:
            return None

    def archive_all_chats_by_user_id(self, user_id: str) -> bool:
        try:
            with get_session() as db:
                db.query(Chat).filter_by(user_id=user_id).update({"archived": True})

            return True
        except:
            return False

    def get_archived_chat_list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> List[ChatModel]:
        with get_session() as db:
            all_chats = (
                db.query(Chat)
                .filter_by(user_id=user_id, archived=True)
                .order_by(Chat.updated_at.desc())
                # .limit(limit).offset(skip)
                .all()
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def get_chat_list_by_user_id(
        self,
        user_id: str,
        include_archived: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ChatModel]:
        with get_session() as db:
            query = db.query(Chat).filter_by(user_id=user_id)
            if not include_archived:
                query = query.filter_by(archived=False)
            all_chats = (
                query.order_by(Chat.updated_at.desc())
                # .limit(limit).offset(skip)
                .all()
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def get_chat_list_by_chat_ids(
        self, chat_ids: List[str], skip: int = 0, limit: int = 50
    ) -> List[ChatModel]:
        with get_session() as db:
            all_chats = (
                db.query(Chat)
                .filter(Chat.id.in_(chat_ids))
                .filter_by(archived=False)
                .order_by(Chat.updated_at.desc())
                .all()
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def get_chat_by_id(self, id: str) -> Optional[ChatModel]:
        try:
            with get_session() as db:
                chat = db.get(Chat, id)
                return ChatModel.model_validate(chat)
        except:
            return None

    def get_chat_by_share_id(self, id: str) -> Optional[ChatModel]:
        try:
            with get_session() as db:
                chat = db.query(Chat).filter_by(share_id=id).first()

                if chat:
                    return self.get_chat_by_id(id)
                else:
                    return None
        except Exception as e:
            return None

    def get_chat_by_id_and_user_id(self, id: str, user_id: str) -> Optional[ChatModel]:
        try:
            with get_session() as db:
                chat = db.query(Chat).filter_by(id=id, user_id=user_id).first()
                return ChatModel.model_validate(chat)
        except:
            return None

    def get_chats(self, skip: int = 0, limit: int = 50) -> List[ChatModel]:
        with get_session() as db:
            all_chats = (
                db.query(Chat)
                # .limit(limit).offset(skip)
                .order_by(Chat.updated_at.desc())
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def get_chats_by_user_id(self, user_id: str) -> List[ChatModel]:
        with get_session() as db:
            all_chats = (
                db.query(Chat)
                .filter_by(user_id=user_id)
                .order_by(Chat.updated_at.desc())
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def get_archived_chats_by_user_id(self, user_id: str) -> List[ChatModel]:
        with get_session() as db:
            all_chats = (
                db.query(Chat)
                .filter_by(user_id=user_id, archived=True)
                .order_by(Chat.updated_at.desc())
            )
            return [ChatModel.model_validate(chat) for chat in all_chats]

    def delete_chat_by_id(self, id: str) -> bool:
        try:
            with get_session() as db:
                db.query(Chat).filter_by(id=id).delete()

                return True and self.delete_shared_chat_by_chat_id(id)
        except:
            return False

    def delete_chat_by_id_and_user_id(self, id: str, user_id: str) -> bool:
        try:
            with get_session() as db:
                db.query(Chat).filter_by(id=id, user_id=user_id).delete()

                return True and self.delete_shared_chat_by_chat_id(id)
        except:
            return False

    def delete_chats_by_user_id(self, user_id: str) -> bool:
        try:
            with get_session() as db:
                self.delete_shared_chats_by_user_id(user_id)

                db.query(Chat).filter_by(user_id=user_id).delete()
            return True
        except:
            return False

    def delete_shared_chats_by_user_id(self, user_id: str) -> bool:
        try:
            with get_session() as db:
                chats_by_user = db.query(Chat).filter_by(user_id=user_id).all()
                shared_chat_ids = [f"shared-{chat.id}" for chat in chats_by_user]

                db.query(Chat).filter(Chat.user_id.in_(shared_chat_ids)).delete()

            return True
        except:
            return False


Chats = ChatTable()
