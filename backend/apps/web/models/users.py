from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time

from utils.utils import decode_token
from utils.misc import get_gravatar_url

from apps.web.internal.db import DB

####################
# User DB Schema
####################


class User(Model):
    id = CharField(unique=True)
    name = CharField()
    email = CharField()
    role = CharField()
    profile_image_url = CharField()
    timestamp = DateField()

    class Meta:
        database = DB


class UserModel(BaseModel):
    id: str
    name: str
    email: str
    role: str = "pending"
    profile_image_url: str = "/user.png"
    timestamp: int  # timestamp in epoch


####################
# Forms
####################


class UserRoleUpdateForm(BaseModel):
    id: str
    role: str


class UsersTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([User])

    def insert_new_user(
        self, id: str, name: str, email: str, role: str = "pending"
    ) -> Optional[UserModel]:
        user = UserModel(
            **{
                "id": id,
                "name": name,
                "email": email,
                "role": role,
                "profile_image_url": get_gravatar_url(email),
                "timestamp": int(time.time()),
            }
        )
        result = User.create(**user.model_dump())
        if result:
            return user
        else:
            return None

    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            user = User.get(User.id == id)
            return UserModel(**model_to_dict(user))
        except:
            return None

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        try:
            user = User.get(User.email == email)
            return UserModel(**model_to_dict(user))
        except:
            return None

    def get_user_by_token(self, token: str) -> Optional[UserModel]:
        data = decode_token(token)

        if data != None and "email" in data:
            return self.get_user_by_email(data["email"])
        else:
            return None

    def get_users(self, skip: int = 0, limit: int = 50) -> List[UserModel]:
        return [
            UserModel(**model_to_dict(user))
            for user in User.select().limit(limit).offset(skip)
        ]

    def get_num_users(self) -> Optional[int]:
        return User.select().count()

    def update_user_role_by_id(self, id: str, role: str) -> Optional[UserModel]:
        try:
            query = User.update(role=role).where(User.id == id)
            query.execute()

            user = User.get(User.id == id)
            return UserModel(**model_to_dict(user))
        except:
            return None


Users = UsersTable(DB)
