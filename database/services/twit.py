import anyio
from anyio import from_thread
from psycopg2 import Error
from sqlalchemy import create_engine, select, func, distinct
from sqlalchemy.connectors import asyncio
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, join, DeclarativeBase
from typing import List, Dict
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
import bcrypt
from websockets import connect
from database.database import engine, session_factory

from fastapi import FastAPI, HTTPException, WebSocket
import uuid
from datetime import datetime

from database.models.users import User, Twit, Comment
from schemas.Twit import CreateTwit, CreateTwitResponse, UserBaseForLikeSchema, TwitBaseSchema, TwitGetDetail, \
    CommentBaseSchema, CreateComment, CommentBaseRespSchema
from fastapi.responses import JSONResponse


class TwitServiceDB:

    def __init__(self):
        self.connections: Dict[uuid.UUID, WebSocket] = {}

    def create_twit(self, data: CreateTwit, user_id: uuid.UUID):

        with session_factory() as session:
            try:
                id = uuid.uuid4()
                twit = Twit(id=id,
                            title=data.title,
                            date=data.date,
                            description=data.description,
                            author_id=user_id,
                            authors_like=[],
                            )
                session.add(twit)
                session.commit()

                user = session.get(User, user_id)

                response = {
                    "id": str(twit.id),
                    "title": twit.title,
                    "date": twit.date,
                    "description": twit.description,
                    "count_like": 0,
                    "author_id": str(twit.author_id),
                    "author_name": user.username,
                    "author_email": user.email,
                    "authors_like": [str(uuid) for uuid in twit.authors_like],
                }

                return JSONResponse(content=response)
            except (Exception, Error) as error:
                print(error)
                return -1

    def get_twit_by_id(self, id: uuid.UUID, user_id: uuid.UUID):
        with session_factory() as session:
            try:
                # Загружаем твит с комментариями и автором
                twit = (
                    session.query(Twit)
                    .options(joinedload(Twit.comments))
                    .filter_by(id=id)
                    .first()
                )
                if not twit:
                    return JSONResponse(content={"error": "Twit not found"}, status_code=404)

                author = session.get(User, twit.author_id)
                if not author:
                    return JSONResponse(content={"error": "Author not found"}, status_code=404)

                authors_like_objects = [
                    UserBaseForLikeSchema(
                        id=user_like.id,
                        username=user_like.username,
                    )
                    for user_like in session.query(User).filter(User.id.in_(twit.authors_like))
                ]

                comments = [
                    CommentBaseSchema(
                        id=comment.id,
                        title=comment.title,
                        date=comment.date,
                        author_id=comment.author_id,
                        author_name=comment.author_name,
                        author_image=comment.author_image,
                    )
                    for comment in twit.comments
                ]

                liked_db = False
                if user_id in twit.authors_like:
                    liked_db = True


                twit_response = TwitGetDetail(
                    id=twit.id,
                    title=twit.title,
                    date=twit.date,
                    description=twit.description,
                    liked=liked_db,
                    count_like=len(authors_like_objects),
                    author_id=twit.author_id,
                    author_name=author.username,
                    author_image=author.image_url,
                    comments=comments,
                )
                return twit_response

            except Exception as error:
                print(f"Error in get_twit_by_id: {error}")
                return JSONResponse(content={"error": str(error)}, status_code=500)

    def get_all_twits(self, user_id: uuid.UUID):
        with session_factory() as session:
            try:
                twits = session.query(Twit).all()
                twit_schemas = []

                for twit in twits:
                    user = session.get(User, twit.author_id)
                    if not user:
                        continue

                    liked_db = False
                    if user_id in twit.authors_like:
                        liked_db = True

                    twit_schemas.append(
                        TwitBaseSchema(
                            id=twit.id,
                            title=twit.title,
                            date=twit.date,
                            description=twit.description,
                            liked=liked_db,
                            count_like=len(twit.authors_like),
                            author_id=user.id,
                            author_name=user.username,
                            author_image=user.image_url
                        )
                    )

                twit_schemas.reverse()
                return twit_schemas
            except Exception as error:
                print(f"Error in get_all_twits: {error}")
                return JSONResponse(content={"error": str(error)}, status_code=408)

    def update_twit(self, twit_id: uuid.UUID, data, user_id: uuid.UUID):
        try:
            with session_factory() as session:

                twit = session.query(Twit).filter(Twit.id == twit_id).first()
                if not twit:
                    raise HTTPException(status_code=404, detail="Twit not found")

                if str(twit.author_id) != str(user_id):
                    raise HTTPException(status_code=403, detail="You do not have permission to update this twit")

                user_db = session.query(User).filter(User.id == user_id).first()

                liked_db = False
                if user_id in twit.authors_like:
                    liked_db = True

                twit_resp = TwitBaseSchema(
                    id=twit.id,
                    title=data.title,
                    date=data.date,
                    description=data.description,
                    liked=liked_db,
                    count_like=len(twit.authors_like),
                    author_id=user_db.id,
                    author_name=user_db.username,
                    author_image=user_db.image_url
                )
                twit.title = data.title
                twit.description = data.description
                twit.date = data.date

                session.commit()
                session.refresh(twit)
                return twit_resp


        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def delete_twit(self, twit_id, user_id):
        with session_factory() as session:
            try:
                twit_db = session.query(Twit).filter(Twit.id == twit_id).first()
                if str(twit_db.author_id) != str(user_id):
                    raise HTTPException(status_code=403, detail="You do not have permission to update this twit")

                session.delete(twit_db)
                session.commit()
                return 0
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def create_comment(self, twit_id, data: CreateComment, user_id):
        with session_factory() as session:
            try:

                twit_db = session.query(Twit).filter(Twit.id == twit_id).first()
                if not twit_db:
                    raise HTTPException(status_code=404, detail="Твит не найден")


                user_db = session.query(User).filter(User.id == user_id).first()
                id = uuid.uuid4()
                comment_db = Comment(
                    id=id,
                    title=data.title,
                    date=data.date,
                    author_id=user_id,
                    author_name=user_db.username,
                    author_image=user_db.image_url,
                    twit_id=twit_id
                )
                session.add(comment_db)
                session.commit()

                comment_resp = CommentBaseRespSchema(
                    id=id,
                    title=data.title,
                    date=data.date,
                    author_id=user_id,
                    author_name=user_db.username,
                    author_image=user_db.image_url,
                    twit_id=twit_id
                )

                from_thread.run(self.send_notification, twit_db.author_id, twit_id, comment_resp)

                return comment_resp
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    async def send_notification(self, author_id, twit_id, comment_resp):
        if author_id in self.connections:
            websocket = self.connections[author_id]
            try:
                notification = {
                    "type": "Новый комментарий",
                    "twit_id": str(twit_id),
                    "comment": comment_resp.title
                }
                await websocket.send_json(notification)
            except Exception as ws_error:
                print(f"Ошибка отправки уведомления: {ws_error}")


twit_service_db: TwitServiceDB = TwitServiceDB()
