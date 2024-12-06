

from fastapi import APIRouter, Cookie
from uuid import UUID

from schemas.Twit import CreateTwit, CreateTwitResponse, TwitBaseSchema, TwitGetDetail, StatusResp, CommentBaseRespSchema, CreateComment
from services.twit import twit_service

from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.post(
    "/twit",
    tags=["Twits"],
    response_model=CreateTwitResponse,
)
def create_twit(data: CreateTwit, access_token: str = Cookie(None)):
    return twit_service.create_twit(data, access_token)


@router.get(
    "/twits",
    tags=["Twits"],
    response_model=list[TwitBaseSchema]
)
def get_all_twits(access_token: str = Cookie(None)):
    return twit_service.get_twits(access_token)


@router.get(
    "/twit/{id}",
    tags=["Twits"],
    response_model=TwitGetDetail
)
def get_twit_by_id(id: UUID, access_token: str = Cookie(None)):
    return twit_service.get_twit_by_id(access_token, id)


@router.put(
    "/twit/{id}",
    tags=["Twits"],
    response_model=TwitBaseSchema
)
def update_twit(id: UUID, data: CreateTwit, access_token: str = Cookie(None)):
    return twit_service.update_twit(id, data, access_token)


@router.delete(
    "/twit/{id}",
    tags=["Twits"],
    response_model=StatusResp
)
def delete_twit(id: UUID, access_token: str = Cookie(None)):
    return twit_service.delete_twit(id, access_token)


@router.post(
    "/comment",
    tags=["Comment"],
    response_model=CommentBaseRespSchema
)
def create_comment(twit_id, data: CreateComment, access_token: str = Cookie(None)):
    return twit_service.create_comment(twit_id, data, access_token)
