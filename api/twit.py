from fastapi import APIRouter, Cookie

from schemas.Twit import CreateTwit, CreateTwitResponse
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
    response_model=list[CreateTwitResponse]
)
def get_all_twits(access_token: str = Cookie(None)):
    return twit_service.get_twits(access_token)

