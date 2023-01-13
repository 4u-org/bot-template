from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from pathlib import Path

from aiogram import Bot, types
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data

from web.utils import Routes

routes = Routes("/inline_demo")

@routes.get("/")
async def demo_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "index.html")

@routes.post("/checkData")
async def check_data_handler(request: Request):
    bot: Bot = request.app["bot"]

    data = await request.post()
    if check_webapp_signature(bot.token, data["_auth"]):
        return json_response({"ok": True})
    return json_response({"ok": False, "err": "Unauthorized"}, status=401)

@routes.post("/sendMessage")
async def send_message_handler(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)

    print(data)
    reply_markup = None
    if data["with_webview"] == "1":
        reply_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Open",
                        web_app=types.WebAppInfo(url=str(request.url.with_scheme("https"))),
                    )
                ]
            ]
        )
    await bot.answer_web_app_query(
        web_app_query_id=web_app_init_data.query_id,
        result=types.InlineQueryResultArticle(
            id=web_app_init_data.query_id,
            title="Demo",
            input_message_content=types.InputTextMessageContent(
                message_text="Hello, World!",
                parse_mode=None,
            ),
            reply_markup=reply_markup,
        ),
    )
    return json_response({"ok": True})