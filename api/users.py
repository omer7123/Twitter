import uuid

from fastapi import APIRouter, Cookie, Depends, UploadFile, File
from schemas.users import Creds, Reg, ResetPassword, UpdateUser, AuthToken, UserResponse, UserData
from services.users import user_service
from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.post(
    "/users/reg",
    tags=["Users"],
    response_model=UserResponse,
)
def register_user(data: Reg, response: Response):
    return user_service.register(data, response)


@router.post(
    "/users/auth",
    tags=["Users"],
    response_model=UserResponse,
)
def auth_user(data: Creds, response: Response):
    return user_service.authorization(data, response)


@router.post(
    "/users/auth_token",
    tags=["Users"],
    response_model=UserResponse,
)
def auth_token_user(data: AuthToken, response: Response):
    return user_service.authorization_token(data, response)


@router.post("/upload_user_image", tags=["Users"],)
def upload_user_image(file: UploadFile = File(...), access_token: str = Cookie(None)):
    return user_service.upload_image(file, access_token)






