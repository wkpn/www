from starlette.responses import RedirectResponse


async def error_404_not_found(
    request, exception
) -> RedirectResponse:
    return RedirectResponse(url="/")
