from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from pathlib import Path

from aiogram import Bot, types
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data

from web.utils import Routes

routes = Routes("/reply_demo")

@routes.get("/")
async def demo_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "static" / "index.html")
    
routes.static(prefix="/", path=Path(__file__).parent.resolve() / "static")