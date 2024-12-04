import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

import pydantic
import uuid


class CreateTwit(pydantic.BaseModel):
    title: str
    date: str
    description: str


class EditTwit(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True


class TwitBaseSchema(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str
    count_like: int
    author_id: uuid.UUID
    author_name: str
    author_image: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserBaseForLikeSchema(pydantic.BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        from_attributes = True


class CreateTwitResponse(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str
    count_like: int
    author_id: uuid.UUID
    author_name: str
    author_email: str
    authors_like: list[UserBaseForLikeSchema]

    class Config:
        orm_mode = True
        from_attributes = True


class CommentBaseSchema(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    author_id: uuid.UUID
    author_name: str
    author_image: str

    class Config:
        orm_mode = True
        from_attributes = True


class TwitGetDetail(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str
    count_like: int
    author_id: uuid.UUID
    author_name: str
    author_image: str
    comments: list[CommentBaseSchema]

    class Config:
        orm_mode = True
        from_attributes = True



