from psycopg2 import Error
from sqlalchemy import create_engine, select, func, distinct
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, join, DeclarativeBase
from typing import List
from sqlalchemy.exc import NoResultFound
import bcrypt


from database.database import engine, session_factory

from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime

from database.models.users import User, Twit
from schemas.Twit import CreateTwit, CreateTwitResponse
from fastapi.responses import JSONResponse

class TwitServiceDB:


    def create_twit(self, data: CreateTwit, user_id: uuid.UUID):

        with session_factory() as session:
            try:
                id = uuid.uuid4()
                twit = Twit(id=id,
                             title=data.title,
                             date=data.date,
                             description=data.description,
                             count_like=0,
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
                    "count_like": twit.count_like,
                    "author_id": str(twit.author_id),
                    "author_name": user.username,
                    "author_email": user.email,
                    "authors_like": [str(uuid) for uuid in twit.authors_like],
                }

                return JSONResponse(content=response)
            except (Exception, Error) as error:
                print(error)
                return -1

    def get_all_twits(self, user_id: uuid.UUID):
        with session_factory() as session:
            try:
                # Получаем все твиты
                twits = session.query(Twit).all()

                response = []
                for twit in twits:
                    user = session.get(User, twit.author_id)  # Получаем данные об авторе твита

                    # Формируем ответ в соответствии с Pydantic моделью
                    twit_response = CreateTwitResponse(
                        id=twit.id,
                        title=twit.title,
                        date=twit.date,
                        description=twit.description,
                        count_like=twit.count_like,
                        author_id=str(twit.author_id),
                        author_name=user.username,
                        author_email=user.email,
                        authors_like=[str(uuid) for uuid in twit.authors_like],  # Преобразуем UUID в строки
                    )
                    response.append(twit_response)

                return response  # FastAPI автоматически сериализует этот список в JSON
            except Exception as error:
                print(error)
                return JSONResponse(content={"error": str(error)}, status_code=500)



twit_service_db: TwitServiceDB = TwitServiceDB()