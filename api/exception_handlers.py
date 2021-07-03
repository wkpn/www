from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse


async def error_404_not_found(
    request: Request,
    exc: HTTPException
) -> RedirectResponse:
    return RedirectResponse(url="/")
