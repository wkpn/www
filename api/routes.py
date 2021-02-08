from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .settings import BASE_DIR
from .views import index, ip


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
