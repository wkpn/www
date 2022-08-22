from starlette.templating import Jinja2Templates
from typing import Dict

from .settings import BASE_DIR


index_data: Dict[str, str] = {
    # data
    "title": "wkpn",
    "name": "Egor Dediulin",
    "description": "Senior Software Engineer at Grid Dynamics",
    "image": "/images/profile_3.jpg",
    # urls
    "github_url": "https://github.com/wkpn",
    "telegram_url": "https://t.me/wkpnbot",
    "linkedin_url": "https://linkedin.com/in/wkpn",
    "signal_number": "tel:+43-670-3081866"
}

templates: Jinja2Templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
