from fastapi import HTTPException

from services.auth import verify_token


def check_token(access_token: str):
    if not access_token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы!")
    token_data = verify_token(access_token)

    if token_data == 'Token has expired':
        raise HTTPException(status_code=401, detail="Время сессии истекло!")
    elif token_data == 'Invalid token':
        raise HTTPException(status_code=401, detail="Вы не авторизованы!")

    return token_data