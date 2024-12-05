import datetime
from typing import List, Optional

import pydantic
import uuid


class Creds(pydantic.BaseModel):
    email: str
    password: str


class Reg(pydantic.BaseModel):
    email: str
    username: str
    password: str
    confirm_password: str


class UpdateUserSchema(pydantic.BaseModel):
    username: str
    email: str
    city: str
    hobby: str
    first_name: str
    last_name: str


class UserResponse(pydantic.BaseModel):
    user_id: uuid.UUID
    email: str
    username: str
    token: str


class TwitForUserData(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str
    liked: bool
    count_like: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserData(pydantic.BaseModel):
    id: uuid.UUID
    username: str
    email: str
    city: str
    hobby: str
    first_name: str
    last_name: str
    image_url: str
    twits: list[TwitForUserData]

    class Config:
        orm_mode = True
        from_attributes = True


class AuthToken(pydantic.BaseModel):
    token: str
