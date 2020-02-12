from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


app = Starlette()

app.mount('/css', StaticFiles(directory='css'), name='css')
app.mount('/images', StaticFiles(directory='images'), name='images')
app.mount('/js', StaticFiles(directory='js'), name='js')
app.mount('/icon', StaticFiles(directory='icon'), name='icon')

templates = Jinja2Templates(directory='templates')

index_data = {
    'title': 'why\'',
    'name': 'Egor Nosov',
    'position': 'Python Developer at Grid Dynamics',
    'image': '/images/avatar.jpg'
}

error_page_data = {
    'title': 'Page not found',
    'error_message': 'Page \'{url}\' could not be found'
}


@app.route('/', methods=['GET'])
async def index(request: Request):
    """
        Basic index page with social links and brief information
    """
    template = 'index.html'
    context = {'request': request}
    context.update(index_data)

    return templates.TemplateResponse(template, context)


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

    return templates.TemplateResponse(template, context, status_code=404)
