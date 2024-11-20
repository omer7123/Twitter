import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException

# Функция для генерации JWT токена
def generate_token(user_id):
    # Установка срока действия токена (1 час)
    expiry = datetime.utcnow() + timedelta(hours=1)

    # Создание токена с идентификатором пользователя и сроком действия
    token = jwt.encode({'user_id': str(user_id), 'exp': expiry}, 'secret_key', algorithm='HS256')

    return token

# Функция для проверки JWT токена
def verify_token(token):
    try:
        # Проверка токена и декодирование его содержимого
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Обработка исключения при истечении срока действия токена
        raise HTTPException(status_code=401, detail="Время сессии истекло!")
    except jwt.InvalidTokenError:
        # Обработка других недопустимых токенов
        raise HTTPException(status_code=401, detail="Вы не авторизованы!")

