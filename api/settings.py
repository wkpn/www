from pathlib import Path
from starlette.config import Config
from typing import Tuple


BASE_DIR: str = str(Path(__file__).parent)

# config variables

config: Config = Config(f"{BASE_DIR}/.env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

ip_info_token: str = config("IP_INFO_TOKEN")
ip_info_url: str = config("IP_INFO_URL")

tg_bot_token: str = config("TG_BOT_TOKEN")
tg_channel_id: int = config("TG_CHANNEL_ID", cast=int)

# miscellaneous

countries: Tuple[str, ...] = (
    "PL",  # Poland
    "RU",  # Russia
)

organizations: Tuple[str, ...] = (
    "AS47764",   # LLC VK
    "AS13238",   # YANDEX LLC
    "AS208722",  # Global DC Oy
)

tg_bot_url: str = f"https://api.telegram.org/bot{tg_bot_token}"

