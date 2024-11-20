from fastapi.middleware.cors import CORSMiddleware
from api import router
from app.app import app

app.include_router(router)

origins = [
    "https://xn--c1ajjlbco7a.xn----gtbbcb4bjf2ak.xn--p1ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"]
)