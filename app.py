from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from data import index_data, error_page_data


def build_application():
    app = Starlette()

    for directory in ('css', 'images', 'js', 'icon'):
        app.mount(f'/{directory}', StaticFiles(directory=directory), name=directory)

    templates = Jinja2Templates(directory='templates')

    @app.route('/', methods=['GET'])
    async def index(request: Request):
        """
            Basic index page with social links and brief information
        """
        template = 'index.html'
        context = {'request': request}
        context.update(index_data)

        return templates.TemplateResponse(name=template, context=context)

    @app.exception_handler(exc_class_or_status_code=404)
    async def not_found(request: Request, exc: HTTPException):
        """
            Friendly 404 page with a rocket animation
        """
        template = '404.html'
        context = {
            'request': request,
            'request_url': request.url.path
        }
        context.update(error_page_data)

        return templates.TemplateResponse(name=template, context=context, status_code=404)

    return app


app = build_application()