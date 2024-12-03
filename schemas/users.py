import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

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


class UserResponse(pydantic.BaseModel):
    user_id: uuid.UUID
    email: str
    username: str
    token: str


class ResetPassword(pydantic.BaseModel):
    email: str


class UpdateUser(pydantic.BaseModel):
    birth_date: datetime.date
    gender: str
    username: str
    request: List[int]
    city: str
    description: str
    department: str
    type: int

class Inquiry(pydantic.BaseModel):
    text: str
    id: int
class UserData(pydantic.BaseModel):
    birth_date: Optional[datetime.date] = None
    gender: Optional[str] = None
    username: Optional[str] = None
    request: Optional[List[Inquiry]] = None
    city: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    type: Optional[int] = None


class AuthToken(pydantic.BaseModel):
    token: str


class Psychologist(pydantic.BaseModel):
    username: str
    title: str
    document: str
    description: str
    city: str
    online: bool
    face_to_face: bool
    gender: str
    birth_date: datetime.date
    request: List[int]
    department: str


class Manager(pydantic.BaseModel):
    username: str
    description: str
    city: str
    company: str
    online: bool
    gender: str
    birth_date: datetime.date

class GiveTask(pydantic.BaseModel):
    text: str
    user_id: uuid.UUID
    test_title: str
    test_id: uuid.UUID

class TaskId(pydantic.BaseModel):
    task_id: uuid.UUID

class GiveTaskAllClient(pydantic.BaseModel):
    text: str
    test_id: uuid.UUID

class GiveTaskListClient(pydantic.BaseModel):
    text: str
    test_id: uuid.UUID
    list_client: List[uuid.UUID]