from starlette.background import BackgroundTask
from starlette.requests import Request

from .helpers import get_ip_info
from .resources import index_data, templates
from .settings import tg_channel_id, DEBUG


async def index(request: Request) -> templates.TemplateResponse:
    template = "index.html"
    context = {"request": request, **index_data}

    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", None)

    background = BackgroundTask(
        get_ip_info,
        chat_id=tg_channel_id,
        ip_address=ip_address,
        user_agent=user_agent
    ) if not DEBUG else None

    return templates.TemplateResponse(
        name=template, context=context, background=background
    )
