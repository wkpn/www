from pathlib import Path
from starlette.config import Config


BASE_DIR: str = str(Path(__file__).parent)

config: Config = Config(f"{BASE_DIR}/.env")

ip_info_token: str = config("IP_INFO_TOKEN")
ip_info_url: str = config("IP_INFO_URL")

tg_bot_token: str = config("TG_BOT_TOKEN")
tg_channel_id: int = config("TG_CHANNEL_ID", cast=int)

tg_bot_url: str = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"

DEBUG: bool = config("DEBUG", cast=bool, default=False)
