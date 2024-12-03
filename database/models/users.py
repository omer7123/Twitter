import enum
import uuid

from database.database import Base
from sqlalchemy import ForeignKey, Enum, Column, String, Boolean, Text, TIMESTAMP, DateTime, func, ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    city: Mapped[str]
    hobby: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    image_url: Mapped[str] = mapped_column(String, nullable=True)

class Twit(Base):
    __tablename__ = "twit"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    authors_like: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID))


class Token(Base):
    __tablename__ = "token"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str]
    exp_date: Mapped[datetime.datetime]