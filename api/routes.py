from starlette.responses import FileResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .settings import BASE_DIR
from .views import index


routes = [
    # main page
    Route("/", index, methods=["GET"]),

    # keybase proof
    Route(
        "/keybase.txt",
        FileResponse(f"{BASE_DIR}/files/keybase.txt"),
        methods=["GET"]
    ),

    # static stuff
    Mount("/css", StaticFiles(directory=f"{BASE_DIR}/css")),
    Mount("/icon", StaticFiles(directory=f"{BASE_DIR}/icon")),
    Mount("/images", StaticFiles(directory=f"{BASE_DIR}/images")),
    Mount("/js", StaticFiles(directory=f"{BASE_DIR}/js"))
]
