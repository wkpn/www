from httpx import AsyncClient
from typing import Dict, Union

from .settings import url

import hashlib
import hmac


def check_hash(data: Dict[str, Union[str, int]], bot_token: str) -> bool:
    telegram_hash = data.pop("hash", None)

    alphabetical_order = sorted(data.items(), key=lambda x: x[0])

    result = "\n".join(f"{k[0]}={k[1]}" for k in alphabetical_order)

    key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(key, msg=result.encode(), digestmod=hashlib.sha256).hexdigest()

    if telegram_hash == computed_hash:
        return True
    return False


async def telegram_send(client: AsyncClient, chat_id: int, text: str) -> None:
    await client.post(url=url, json={
        "chat_id": chat_id,
        "text": text
    })
