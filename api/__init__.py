from fastapi import APIRouter
from api import example

router = APIRouter()

router.include_router(example.router)