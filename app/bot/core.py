import asyncio
from app.config import RUNNING_MODE, WEBHOOK_URL
from app.bot.api import BotAPI
from app.bot.handlers import handle_update
from fastapi import Request
from datetime import datetime
from ..config import debugging_mode
from .handle_users import user_login
# import .config

bot_api = BotAPI()

last_update_id = None

async def polling_loop():
    global last_update_id
    while True:
        try:
            updates_resp = await bot_api.get_updates(offset=last_update_id, timeout=20)   
            # print(updates_resp) 
            if "result" in updates_resp:
                for update in updates_resp["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    await user_login(update["message"]["from"])
                    await handle_update(update)
                    
                    print(
                        "Got New Message Form ",
                        updates_resp["result"][0]["message"]["from"]["username"],
                        datetime.now(),
                    )
        except Exception as e:
            if debugging_mode == True:
                print("Error in polling:", datetime.now(), e)
                # traceback.print_exc()  # چاپ کامل استک‌ترس
        await asyncio.sleep(2)


async def handle_webhook(request: Request):
    data = await request.json()
    await handle_update(data)
    return {"ok": True}

