from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from .settings import secret_key


middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key)
]
