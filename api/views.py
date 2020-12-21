from starlette.background import BackgroundTask
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from .helpers import get_ip_info
from .resources import index_data, templates
from .settings import tg_channel_id


async def error(request: Request, exc: HTTPException) -> RedirectResponse:
    return RedirectResponse(url="/")


async def index(request: Request) -> templates.TemplateResponse:
    template = "index.html"
    context = {
        "request": request,
        **index_data
    }

    user_agent = request.headers.get("user-agent", None)
    ip_address = request.client.host

    background = BackgroundTask(get_ip_info,
                                client=request.app.state.client,
                                chat_id=tg_channel_id,
                                ip_address=ip_address,
                                user_agent=user_agent)

    return templates.TemplateResponse(name=template, context=context, background=background)


async def ip(request: Request) -> PlainTextResponse:
    return PlainTextResponse(request.client.host)
