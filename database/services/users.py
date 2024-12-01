import os

from psycopg2 import Error
from sqlalchemy import create_engine, select, func, distinct
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, join, DeclarativeBase
from typing import List
from sqlalchemy.exc import NoResultFound
import bcrypt
from starlette.responses import JSONResponse

from database.database import engine, session_factory

from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime

from database.models.users import User

UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



class UserServiceDB:


    def register_user(self, id, username, email, password):
        with session_factory() as session:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User(id=id,
                             username=username,
                             email=email,
                             password=hashed_password.decode('utf-8'),
                             city="",
                             hobby="",
                             first_name="",
                             last_name="",
                             )
                session.add(user)
                session.commit()
                return 0
            except (Exception, Error) as error:
                # print(error)
                return -1

    def check_user(self, email, password):
        with session_factory() as session:
            try:
                user = session.query(User).filter_by(email=email).one()
                hashed_password = user.password.encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return 0
                else:
                    return -1

            except (Exception, Error) as error:
                print(error)
                return -1

    def get_user(self, email):
        with session_factory() as session:
            try:
                user = session.query(User).filter_by(email=email).one()

                return user

            except (Exception, Error) as error:
                print(error)
                return -1

    def upload_image(self, file, user_id):
        with session_factory() as session:
                try:
                    user = session.get(User, user_id)  # Асинхронный запрос к базе данных
                    if not user:
                        raise HTTPException(status_code=404, detail="User not found")

                    # Генерация уникального имени для файла
                    file_extension = file.filename.split('.')[-1]
                    file_name = f"{uuid.uuid4()}.{file_extension}"
                    file_path = os.path.join(UPLOAD_FOLDER, file_name)

                    # Асинхронное чтение файла
                    with open(file_path, "wb") as buffer:
                        content = file.read()
                        buffer.write(content)

                    # Сохраняем URL изображения в базе данных
                    user.image_url = f"/images/{file_name}"
                    session.commit()  # Асинхронный commit

                    return JSONResponse(content={"image_url": user.image_url})

                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


user_service_db: UserServiceDB = UserServiceDB()