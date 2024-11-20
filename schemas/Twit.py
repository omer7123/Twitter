import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

import pydantic
import uuid


class CreateTwit(pydantic.BaseModel):
    title: str
    date: str
    description: str


class CreateTwitResponse(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    date: str
    description: str
    count_like: int
    author_id: str
    author_name: str
    author_email: str
    authors_like: list[uuid.UUID]

    class Config:
        from_attributes = True

