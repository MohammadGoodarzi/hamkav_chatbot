import httpx
from app.config import BOT_TOKEN, API_BASE_URL

class BotAPI:
    def __init__(self):
        self.base_url = f"{API_BASE_URL}/bot{BOT_TOKEN}"

    async def send_message(self, chat_id: int, text: str, reply_markup: dict = None):
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            data["reply_markup"] = reply_markup

        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/sendMessage", json=data)
            resp.raise_for_status()
            return resp.json()

    async def get_updates(self, offset=None, timeout=30):
        params = {"timeout": timeout}
        if offset:
            params["offset"] = offset

        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/getUpdates", params=params)
            resp.raise_for_status()
            return resp.json()
