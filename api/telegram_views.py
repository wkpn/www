from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from typing import Union

from .helpers import check_hash, telegram_send
from .resources import templates
from .settings import (
    tg_bot_token,
    tg_bot_username,
    tg_user_id,
)

import json


async def telegram(request: Request) -> templates.TemplateResponse:
    telegram_user = request.session.get("telegram_user")
    template = "telegram.html"

    if telegram_user:
        context = {
            "request": request,
            "button": False,
            **telegram_user
        }
    else:
        context = {
            "request": request,
            "button": True,
            "tg_bot_username": tg_bot_username
        }
    return templates.TemplateResponse(name=template, context=context)


async def telegram_auth(request: Request) -> Union[PlainTextResponse, RedirectResponse]:
    params = request.query_params

    _dict = params._dict
    _check = check_hash(_dict, tg_bot_token)

    if not _check:
        return PlainTextResponse("Invalid checksum")

    background = None
    telegram_user = request.session.get("telegram_user")

    if not telegram_user and params:
        first_name = params.get("first_name", "")
        last_name = params.get("last_name", "")
        name = f"{first_name} {last_name}".strip()

        del first_name, last_name

        username = params.get("username", "")
        user_id = params.get("id")

        photo_url = params.get("photo_url", "/images/default.png")

        session_data = dict(name=name,
                            username=username,
                            user_id=user_id,
                            photo_url=photo_url)

        request.session["telegram_user"] = session_data

        background = BackgroundTask(telegram_send,
                                    client=request.app.state.client,
                                    chat_id=tg_user_id,
                                    text=f"Auth: {json.dumps(session_data)}")

    return RedirectResponse(url="/telegram", background=background)


async def telegram_form(request: Request) -> PlainTextResponse:
    req_form = await request.form()
    telegram_message = req_form["message"]

    telegram_user = request.session.get("telegram_user")

    sender = telegram_user["user_id"]
    if telegram_user["username"]:
        sender = f"@{telegram_user['username']}"

    background = BackgroundTask(telegram_send,
                                client=request.app.state.client,
                                chat_id=tg_user_id,
                                text=f"From: {sender}\n"
                                     f"Text: {telegram_message}")

    return PlainTextResponse("Message sent!", background=background)


async def telegram_logout(request: Request) -> RedirectResponse:
    telegram_user = request.session.get("telegram_user")
    background = None

    if telegram_user:
        background = BackgroundTask(telegram_send,
                                    client=request.app.state.client,
                                    chat_id=tg_user_id,
                                    text=f"Logout: {json.dumps(telegram_user)}"
                                    )
        request.session.pop("telegram_user", None)

    return RedirectResponse(url="/telegram", background=background)
