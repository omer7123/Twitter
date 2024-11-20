from typing import re

from schemas.users import Creds, Reg, ResetPassword, UpdateUser, UserResponse, UserData
from database.services.users import user_service_db

from services.auth import generate_token
import uuid
from starlette.responses import Response
from smtplib import SMTPRecipientsRefused
from psycopg2 import Error
from fastapi import FastAPI, HTTPException
from utils.token_utils import check_token


app = FastAPI()

class UserService:

    def get_users(self, access_token) -> list or str:
        token_data = check_token(access_token)

        role = user_service_db.check_role(uuid.UUID(token_data['user_id']))

        if role == 0:
            items = user_service_db.get_all_users()
            return items
        else:
            raise HTTPException(status_code=403, detail="У вас недостаточно прав для выполнения данной операции!")


    def get_data_user(self, access_token: str) -> UserData:
        try:
            token_data = check_token(access_token)
            user_id = uuid.UUID(token_data['user_id'])

            user_data = user_service_db.get_data_user(user_id)
            if user_data is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            return UserData(**user_data)

        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Некорректный токен: {ve}")
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")


    def authorization(self, payload: Creds, response: Response):
         if user_service_db.check_user(payload.email, payload.password) == 0:
            user = user_service_db.get_user(payload.email)
            if user == -1:
                raise HTTPException(status_code=404,
                                    detail="Пользователя с такими данными не найдено!")
            print(user)
            token = generate_token(user.id)
            response.set_cookie(key="access_token", value=token, httponly=True)

            return {
                "user_id": user.id,
                "email": user.email,
                "username": user.username
            }
         else:
             raise HTTPException(status_code=404, detail="Пользователя с такими данными не найдено!")


    def authorization_token(self, payload, response: Response):

        user = user_service_db.get_user_by_token(payload.token)
        if user == 0:
            raise HTTPException(status_code=400, detail="Не валидный токен!")
        token = generate_token(user.id)
        response.set_cookie(key="access_token", value=token, httponly=True)
        user_service_db.add_token_db(user.id, token)
        return {
            "user_id": user.id,
            "email": user.email,
            "username": user.username
        }

    def register(self, payload: Reg, response: Response) -> UserResponse:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, payload.email):
            if payload.password == payload.confirm_password:
                user_id = uuid.uuid4()
                if user_service_db.register_user(user_id, payload.username, payload.email, payload.password) == 0:
                    token = generate_token(user_id)
                    new_user = UserResponse(user_id=user_id, email=payload.email, username=payload.username)
                    response.set_cookie(key="access_token", value=token, httponly=True)

                    return new_user
                else:
                    raise HTTPException(status_code=409, detail="Пользователь с таким адресом электронной почты уже зарегистрирован")
            else:
                raise HTTPException(status_code=400, detail="Пароли не совпадают!")
        else:
            raise HTTPException(status_code=408, detail="Почта неверна")



    def update_user(self, payload: UpdateUser, access_token):
        token_data = check_token(access_token)

        try:
            if (21 > payload.type) and (payload.type > 0):
                user_service_db.update_user_db(token_data['user_id'], payload.username, payload.gender, payload.birth_date,
                                                payload.request, payload.city, payload.description, payload.department, payload.type)
                return "Successfully"
            else:
                raise HTTPException(status_code=400, detail="Тип пользователя введен неверно!")
        except(Error):
            raise HTTPException(status_code=500, detail="Что-то пошло не так!")

#sdfb




user_service: UserService = UserService()
