from starlette.templating import Jinja2Templates
from typing import Dict

from .settings import BASE_DIR


index_data: Dict[str, str] = {
    "title": "wkpn",
    "name": "Egor D.",
    "description": "Software Engineer",
    "image": "/images/profile_2.jpg",
    # urls
    "github_url": "https://github.com/wkpn",
    "telegram_url": "https://t.me/wkpnbot",
    "linkedin_url": "https://www.linkedin.com/in/wkpn",
    "signal_number": "tel:+43-670-3081866"
}

templates: Jinja2Templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
