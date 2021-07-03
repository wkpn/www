from aiohttp import ClientSession
from typing import Any, Dict, Optional, Tuple

from .settings import (
    ip_info_token,
    ip_info_url,
    organizations,
    tg_bot_url
)


async def get_ip_info(
    chat_id: int,
    ip_address: str,
    user_agent: Optional[str] = None
) -> None:
    url = f"{ip_info_url}/{ip_address}?token={ip_info_token}"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()

        country, text, organization = _prepare_message_text(
            ip_address, response, user_agent
        )
        message = await _tg_post(
            session,
            "sendMessage",
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=True,
            parse_mode="HTML"
        )

        message_id = message["message_id"]

        if country == "RU":
            if not any(org in organization for org in organizations):
                await _tg_post(
                    session,
                    "pinChatMessage",
                    chat_id=chat_id,
                    message_id=message_id
                )


def _prepare_message_text(
    ip_address: str,
    response: Dict[str, Any],
    user_agent: Optional[str] = None,
) -> Tuple[str, str, str]:
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
    return country, text, organization


async def _tg_post(
    session: ClientSession, method: str, **kwargs: Any
) -> Dict[str, Any]:
    async with session.post(
        url=f"{tg_bot_url}/{method}",
        json=kwargs
    ) as response:
        return (await response.json())["result"]
