from starlette.templating import Jinja2Templates
from typing import Dict

from .settings import BASE_DIR


index_data: Dict[str, str] = {
    "title": "wkpn",
    "name": "Egor D.",
    "description": "Software Engineer at EPAM Systems",
    "image": "/images/profile.jpg",
    # urls
    "github_url": "https://github.com/wkpn",
    "telegram_url": "https://t.me/wkpnbot",
    "linkedin_url": "https://www.linkedin.com/in/whyapostrophe",
    "signal_number": "tel:+1-562-352-0058"
}

templates: Jinja2Templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
