import shutil
import uuid

from fastapi import APIRouter, Cookie, Depends, UploadFile, File
from schemas.users import Creds, Reg, AuthToken, UserResponse, UserData, UpdateUserSchema, ImageUrlResp, UserResponseAuth
from services.users import user_service
from starlette.responses import JSONResponse, Response, FileResponse

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
    response_model=UserResponseAuth,
)
def auth_user(data: Creds, response: Response):
    return user_service.authorization(data, response)


@router.post(
    "/users/auth_token",
    tags=["Users"],
    response_model=UserResponseAuth,
)
def auth_token_user(data: AuthToken, response: Response):
    return user_service.authorization_token(data, response)


@router.get(
    "/users/data",
    tags=["Users"],
    response_model=UserData
)
def get_user_data_by_token(access_token: str = Cookie(None)):
    return user_service.get_data_user(access_token)


@router.get(
    "/users/data/{id}",
    tags=["Users"],
    response_model=UserData
)
def get_user_data_by_id(id: uuid.UUID, access_token: str = Cookie(None)):
    return user_service.get_data_user_by_id(id, access_token)


@router.put(
    "/users/data/{id}",
    tags=["Users"],
    response_model=UserData
)
def update_user_data(data: UpdateUserSchema, access_token: str = Cookie(None)):
    return user_service.update_user(data, access_token)


@router.post("/upload_user_image", tags=["Users"], response_model=ImageUrlResp)
async def upload_user_image(file: UploadFile = File(...), access_token: str = Cookie(None)):
    return user_service.upload_image(file, access_token)


@router.get("/image", tags=["Users"])
async def get_user_image(access_token: str = Cookie(None)):
    return user_service.get_image(access_token)

@router.get("/image/{id}", tags=["Users"])
async def get_user_image(path: str, access_token: str = Cookie(None)):
    return user_service.get_image_path(path, access_token)
