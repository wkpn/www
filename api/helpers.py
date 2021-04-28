from httpx import AsyncClient
from typing import Any, Dict, Optional

from .settings import (
    ip_info_token,
    ip_info_url,
    organizations,
    tg_bot_url
)


async def get_ip_info(
    chat_id: int, ip_address: str, user_agent: Optional[str] = None
) -> None:
    url = f"{ip_info_url}/{ip_address}?token={ip_info_token}"

    async with AsyncClient(http2=True) as client:
        response = await client.get(url)
        response = response.json()

        country = response.get("country", None)
        organization = response.get("org", None)

        ip_data = {
            "IP": ip_address,
            "Country": country,
            "Location": response.get("loc", None),
            "Region": response.get("region", None),
            "City": response.get("city", None),
            "Organization": organization,
            "Postal": response.get("postal", None),
            "User-Agent": user_agent
        }

        text = "\n".join(
            f"<b>{k}</b>: {v}" for k, v in ip_data.items() if v
        )

        message = await _tg_post(
            client,
            "sendMessage",
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=True,
            parse_mode="HTML"
        )

        message_id = message["message_id"]

        if country == "RU" and organization not in organizations:
            await _tg_post(
                client,
                "pinChatMessage",
                chat_id=chat_id,
                message_id=message_id
            )


async def _tg_post(
    client: AsyncClient, method: str, **kwargs: Any
) -> Dict[str, Any]:
    response = await client.post(
        url=f"{tg_bot_url}/{method}",
        json=kwargs
    )
    return response.json()["result"]
