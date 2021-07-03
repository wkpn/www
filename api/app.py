from starlette.applications import Starlette

from .routes import routes
from .views import error


def build_application() -> Starlette:
    return Starlette(
        routes=routes,
        exception_handlers={404: error}
    )


app = build_application()
