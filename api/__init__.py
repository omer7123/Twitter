from fastapi import APIRouter

from api.users import router as user_router
from api.twit import router as twit_router

router = APIRouter()

router.include_router(user_router)
router.include_router(twit_router)
