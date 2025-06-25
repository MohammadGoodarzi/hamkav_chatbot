from fastapi import FastAPI, Request
from app.bot.core import polling_loop, handle_webhook
from app.config import RUNNING_MODE, WEBHOOK_URL
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    if RUNNING_MODE == "polling":
        asyncio.create_task(polling_loop())
    elif RUNNING_MODE == "webhook":
        # برای webhook فقط باید webhook روی تلگرام یا بله ست شده باشه
        print(f"Webhook mode active at {WEBHOOK_URL}")

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    if RUNNING_MODE != "webhook":
        return {"error": "Webhook mode is not enabled"}
    return await handle_webhook(request)

@app.get("/")
async def root():
    return {"message": f"Bot is running in {RUNNING_MODE} mode."}
