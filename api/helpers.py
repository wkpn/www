from httpx import AsyncClient
from typing import Any, Optional

from .settings import ip_info_token, ip_info_url, tg_bot_url


async def get_ip_info(
    client: AsyncClient, chat_id: int, ip_address: str, user_agent: Optional[str] = None
) -> None:
    url = f"{ip_info_url}/{ip_address}?token={ip_info_token}"

    response = await client.get(url)
    response = response.json()

    ip_data = {
        "IP": ip_address,
        "Country": response.get("country", None),
        "Location": response.get("loc", None),
        "Region": response.get("region", None),
        "City": response.get("city", None),
        "Organization": response.get("org", None),
        "Postal": response.get("postal", None),
        "User-Agent": user_agent,
    }

    text = "\n".join(
        f"<b>{key}</b>: {value}" for key, value in ip_data.items() if value is not None
    )

    await telegram_send(
        client, chat_id, text, disable_web_page_preview=True, parse_mode="HTML"
    )


async def telegram_send(
    client: AsyncClient, chat_id: int, text: str, **kwargs: Any
) -> None:
    await client.post(url=tg_bot_url, json={"chat_id": chat_id, "text": text, **kwargs})