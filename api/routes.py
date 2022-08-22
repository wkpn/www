from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from typing import List, Union

from .settings import BASE_DIR
from .views import index


routes: List[Union[Route, Mount]] = [
    # main page
    Route("/", index, methods=["GET"]),

    # static stuff
    Mount("/css", StaticFiles(directory=f"{BASE_DIR}/css")),
    Mount("/icon", StaticFiles(directory=f"{BASE_DIR}/icon")),
    Mount("/images", StaticFiles(directory=f"{BASE_DIR}/images")),
    Mount("/js", StaticFiles(directory=f"{BASE_DIR}/js"))
]
