from httpx import AsyncClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from typing import Callable, Dict, List

from .settings import secret_key, BASE_DIR
from .views import error, index, ip


def build_application() -> Starlette:
    routes = [
        # top-level index
        Route("/", index, methods=["GET"]),

        # ip info
        Route("/ip", ip, methods=["GET"]),

        # static stuff
        Mount("/css", StaticFiles(directory=f"{BASE_DIR}/css"), name="css"),
        Mount("/icon", StaticFiles(directory=f"{BASE_DIR}/icon"), name="icon"),
        Mount("/images", StaticFiles(directory=f"{BASE_DIR}/images"), name="images"),
        Mount("/js", StaticFiles(directory=f"{BASE_DIR}/js"), name="js")
    ]

    client: AsyncClient = AsyncClient(http2=True)
    exception_handlers: Dict[int, Callable] = {404: error}
    middleware: List[Middleware, ...] = [Middleware(SessionMiddleware, secret_key=secret_key)]

    app: Starlette = Starlette(routes=routes,
                               middleware=middleware,
                               exception_handlers=exception_handlers)

    app.state.client = client

    return app


app = build_application()
