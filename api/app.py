from starlette.applications import Starlette

from .middleware import middleware
from .routes import routes
from .views import error


def build_application() -> Starlette:
    app = Starlette(
        routes=routes,
        middleware=middleware,
        exception_handlers={404: error}
    )

    return app


app = build_application()
