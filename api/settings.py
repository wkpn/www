from pathlib import Path
from starlette.config import Config


BASE_DIR: str = str(Path(__file__).parent)

config: Config = Config(f"{BASE_DIR}/.env")

secret_key: str = config("SECRET_KEY")
tg_bot_token: str = config("TG_BOT_TOKEN")
tg_bot_username: str = config("TG_BOT_USERNAME")
tg_user_id: int = config("TG_USER_ID", cast=int)

url: str = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
