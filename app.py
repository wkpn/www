from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.config import Config
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from httpx import AsyncClient
from typing import Dict, Union

import hashlib
import hmac
import json
import os


index_data = {
    "title": "why'",
    "name": "Egor Nosov",
    "position": "Software Engineer at EPAM Systems",
    "image": "/images/avatar.jpg"
}


def build_application() -> Starlette:
    config = Config()

    bot = config("TG_BOT")
    bot_token = config("BOT_TOKEN")
    secret_key = config("SECRET_KEY")
    tg_id = config("TG_ID", cast=int)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    templates = Jinja2Templates(directory="templates")

    def _check_hash(data: Dict[str, Union[str, int]], bot_token: str) -> bool:
        telegram_hash = data.pop("hash", None)

        alphabetical_order = sorted(data.items(), key=lambda x: x[0])

        result = "\n".join(f"{k[0]}={k[1]}" for k in alphabetical_order)

        key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(key, msg=result.encode(), digestmod=hashlib.sha256).hexdigest()

        if telegram_hash == computed_hash:
            return True
        return False

    async def _telegram_send(client: AsyncClient, chat_id: int, text: str):
        await client.post(url=url, json={
            "chat_id": chat_id,
            "text": text
        })

    async def index(request: Request) -> templates.TemplateResponse:
        template = "index.html"
        context = {
            "request": request,
            **index_data
        }
        return templates.TemplateResponse(name=template, context=context)

    async def error(request: Request, exc: HTTPException) -> RedirectResponse:
        return RedirectResponse(url="/")

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
                "bot": bot
            }
        return templates.TemplateResponse(name=template, context=context)

    async def telegram_auth(request: Request) -> Union[PlainTextResponse, RedirectResponse]:
        params = request.query_params

        _dict = params._dict
        _check = _check_hash(_dict, bot_token)

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

            background = BackgroundTask(_telegram_send,
                                        client=request.app.state.client,
                                        chat_id=tg_id,
                                        text=f"Auth: {json.dumps(session_data)}")

        return RedirectResponse(url="/telegram", background=background)

    async def telegram_form(request: Request):
        req_form = await request.form()
        telegram_message = req_form["message"]

        telegram_user = request.session.get("telegram_user")
        telegram_username = telegram_user["username"]
        telegram_id = telegram_user["user_id"]

        if telegram_username:
            sender = f"@{telegram_username}"
        else:
            sender = telegram_id

        background = BackgroundTask(_telegram_send,
                                    client=request.app.state.client,
                                    chat_id=tg_id,
                                    text=f"New message:\n\n"
                                         f"From: {sender}\n"
                                         f"Text: {telegram_message}")

        return PlainTextResponse("Message sent!", background=background)

    async def telegram_logout(request: Request) -> RedirectResponse:
        telegram_user = request.session.get("telegram_user")
        background = None

        if telegram_user:
            background = BackgroundTask(_telegram_send,
                                        client=request.app.state.client,
                                        chat_id=tg_id,
                                        text=f"Logout: {json.dumps(telegram_user)}"
                                        )

            request.session.pop("telegram_user", None)

        return RedirectResponse(url="/telegram", background=background)

    routes = [
        # top-level index
        Route("/", index, methods=["GET"]),

        Mount("/telegram", routes=[
            Route("/", telegram, methods=["GET"]),
            Route("/auth", telegram_auth, methods=["GET"]),
            Route("/form", telegram_form, methods=["POST"]),
            Route("/logout", telegram_logout, methods=["GET"]),
        ]),

        # static stuff
        Mount("/css", StaticFiles(directory=os.path.realpath("css")), name="css"),
        Mount("/icon", StaticFiles(directory=os.path.realpath("icon")), name="icon"),
        Mount("/images", StaticFiles(directory=os.path.realpath("images")), name="images"),
        Mount("/js", StaticFiles(directory=os.path.realpath("js")), name="js")
    ]

    exception_handlers = {404: error}
    middleware = [Middleware(SessionMiddleware, secret_key=secret_key)]

    app = Starlette(routes=routes,
                    middleware=middleware,
                    exception_handlers=exception_handlers)

    app.state.client = AsyncClient(http2=True)

    return app


app = build_application()
