from starlette.applications import Starlette

from .exception_handlers import error_404_not_found
from .routes import routes


def build_application() -> Starlette:
    return Starlette(
        routes=routes,
        exception_handlers={404: error_404_not_found}
    )


app = build_application()
