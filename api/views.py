from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from .resources import index_data, templates


async def error(request: Request, exc: HTTPException) -> RedirectResponse:
    return RedirectResponse(url="/")


async def index(request: Request) -> templates.TemplateResponse:
    template = "index.html"
    context = {
        "request": request,
        **index_data
    }
    return templates.TemplateResponse(name=template, context=context)


async def ip(request: Request) -> PlainTextResponse:
    return PlainTextResponse(request.client.host)
