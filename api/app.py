from starlette.applications import Starlette

from .routes import routes
from .views import error


def build_application() -> Starlette:
    app = Starlette(
        routes=routes,
        exception_handlers={404: error}
    )

    return app


app = build_application()
