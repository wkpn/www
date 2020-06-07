from starlette.requests import Request
from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from data import index_data, error_page_data


def build_application() -> Router:
    templates = Jinja2Templates(directory="templates")

    async def index(request: Request) -> templates.TemplateResponse:
        """
        Basic index page with social links and brief information
        """
        template = "index.html"
        context = {
            "request": request,
            **index_data
        }

        return templates.TemplateResponse(name=template, context=context)

    async def error(request: Request) -> templates.TemplateResponse:
        """
        Friendly 404 page with a rocket animation
        """
        template = "404.html"
        context = {
            "request": request,
            "request_url": request.url.path,
            **error_page_data
        }

        return templates.TemplateResponse(name=template, context=context, status_code=404)

    app = Router(routes=[
        Route("/", index, methods=["GET"]),
        Route("/{path}", error, methods=["GET"]),
        Mount("/css", StaticFiles(directory="css"), name="css"),
        Mount("/images", StaticFiles(directory="images"), name="images"),
        Mount("/js", StaticFiles(directory="js"), name="js"),
        Mount("/icon", StaticFiles(directory="icon"), name="icon")
    ])

    return app


app = build_application()
