from pathlib import Path
from starlette.config import Config
from typing import Tuple


BASE_DIR: str = str(Path(__file__).parent)

config: Config = Config(f"{BASE_DIR}/.env")

ip_info_token: str = config("IP_INFO_TOKEN")
ip_info_url: str = config("IP_INFO_URL")

organizations: Tuple[str, ...] = (
    "AS47764",  # mail.ru
    "AS13238",  # yandex.ru
)

tg_bot_token: str = config("TG_BOT_TOKEN")
tg_channel_id: int = config("TG_CHANNEL_ID", cast=int)

tg_bot_url: str = f"https://api.telegram.org/bot{tg_bot_token}"

DEBUG: bool = config("DEBUG", cast=bool, default=False)
