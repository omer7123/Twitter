import os
import shutil
import uuid

import bcrypt
from fastapi import HTTPException
from psycopg2 import Error
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse, FileResponse

from database.database import session_factory
from database.models.users import User, Token
from schemas.users import TwitForUserData, UserData, UpdateUserSchema

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
                            image_url=""
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
        try:
            upload_folder = "uploads/"
            os.makedirs(upload_folder, exist_ok=True)
            file_path = f"{upload_folder}{uuid.uuid4()}"

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)


            with session_factory() as session:
                user = session.query(User).filter(User.id == user_id).first()

                if not user:
                    raise HTTPException(status_code=404, detail="Пользователь не найден")

                user.image_url = file_path
                session.commit()

                return {"url": user.image_url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при загрузке: {e}")

    def get_user_by_token(self, token_id):
        with session_factory() as session:
            try:
                token = session.query(Token).filter_by(token=token_id)
                user_id = token[0].user_id
                user = session.query(User).filter_by(id=user_id).one()
                if user:
                    return user
                else:
                    return 0
            except (Exception, Error) as error:
                print(error)
                return 0

    def add_token_db(self, id, token):
        with session_factory() as session:
            try:
                token = Token(id=uuid.uuid4(),
                              user_id=id,
                              token=token,
                              exp_date=func.now(),
                              )
                session.add(token)
                session.commit()
                return 0
            except (Exception, Error) as error:
                raise HTTPException(status_code=403,
                                    detail="У вас недостаточно прав для выполнения данной операции!")

    def get_data_user(self, user_id, user_id_from_token):
        with session_factory() as session:
            try:

                user_db = session.query(User).filter(User.id == user_id).options(joinedload(User.twits)).first()

                if not user_db:
                    raise HTTPException(status_code=404, detail="Пользователь не найден")

                if user_id_from_token == "":

                    twits_data = [
                        TwitForUserData(
                            id=twit.id,
                            title=twit.title,
                            date=twit.date,
                            description=twit.description,
                            liked=user_id in twit.authors_like,
                            count_like=len(twit.authors_like)
                        ) for twit in user_db.twits
                    ]
                else:
                    twits_data = [
                        TwitForUserData(
                            id=twit.id,
                            title=twit.title,
                            date=twit.date,
                            description=twit.description,
                            liked=user_id_from_token in str(twit.authors_like),
                            count_like=len(twit.authors_like)
                        ) for twit in user_db.twits
                    ]

                resp = UserData(
                    id=user_db.id,
                    username=user_db.username,
                    email=user_db.email,
                    city=user_db.city,
                    hobby=user_db.hobby,
                    first_name=user_db.first_name,
                    last_name=user_db.last_name,
                    image_url=user_db.image_url,
                    twits=twits_data
                )
                return resp
            except(Exception, Error) as err:
                raise HTTPException(status_code=403,
                                    detail="Непредвиденная ошибка")

    def update_user(self, user_id, data: UpdateUserSchema):
        with session_factory() as session:
            try:
                user_db = session.query(User).filter(User.id == user_id).first()
                if not user_db:
                    raise HTTPException(status_code=404, detail="Пользователь не найден")

                user_db.username = data.username
                user_db.email = data.email
                user_db.city = data.city
                user_db.first_name = data.first_name
                user_db.hobby = data.hobby
                user_db.last_name = data.last_name

                session.commit()

                twits_data = [
                    TwitForUserData(
                        id=twit.id,
                        title=twit.title,
                        date=twit.date,
                        description=twit.description,
                        count_like=len(twit.authors_like)
                    ) for twit in user_db.twits
                ]

                resp = UserData(
                    id=user_db.id,
                    username=user_db.username,
                    email=user_db.email,
                    city=user_db.city,
                    hobby=user_db.hobby,
                    first_name=user_db.first_name,
                    last_name=user_db.last_name,
                    image_url=user_db.image_url,
                    twits=twits_data
                )

                return resp
            except(Exception, Error) as err:
                raise HTTPException(status_code=403,
                                    detail="Непредвиденная ошибка")

    def get_image_path(self, path):
        try:
            if path == "":
                raise HTTPException(status_code=404, detail="Изображение не загружено")
            print(path)
            return FileResponse(f"{path}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении изображения: {e}")

user_service_db: UserServiceDB = UserServiceDB()
