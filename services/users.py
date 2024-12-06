

from schemas.users import Creds, Reg, UserResponse, UserData, UpdateUserSchema
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

    def get_data_user(self, access_token: str) -> UserData:
        try:
            token_data = check_token(access_token)
            user_id = uuid.UUID(token_data['user_id'])
            user_data = user_service_db.get_data_user(user_id, "")

            if user_data is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return user_data

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
            user_service_db.add_token_db(user.id, token)
            return {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "token": token
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
            "username": user.username,
            "token": token
        }

    def register(self, payload: Reg, response: Response) -> UserResponse:

        if payload.password == payload.confirm_password:
            user_id = uuid.uuid4()
            if user_service_db.register_user(user_id, payload.username, payload.email, payload.password) == 0:
                token = generate_token(user_id)
                new_user = UserResponse(user_id=user_id, email=payload.email, username=payload.username, token = token)
                response.set_cookie(key="access_token", value=token, httponly=True)

                user_service_db.add_token_db(user_id, token)
                return new_user
            else:
                raise HTTPException(status_code=409, detail="Пользователь с таким адресом электронной почты уже зарегистрирован")
        else:
            raise HTTPException(status_code=400, detail="Пароли не совпадают!")




    def update_user(self, data: UpdateUserSchema, access_token):
        token_data = check_token(access_token)
        return user_service_db.update_user(token_data['user_id'], data)

    def upload_image(self, file, access_token):
        token_data = check_token(access_token)
        return user_service_db.upload_image(file, token_data['user_id'])

    def get_data_user_by_id(self, id, access_token):
        data_token=check_token(access_token)
        return user_service_db.get_data_user(id, data_token['user_id'])

    def get_image(self, access_token):
        data_token = check_token(access_token)
        return user_service_db.get_image(data_token['user_id'])


user_service: UserService = UserService()
