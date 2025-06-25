from app.bot.api import BotAPI

bot_api = BotAPI()

async def handle_update(update: dict):
    # فقط پیام‌های متنی ساده بررسی می‌کنیم
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        # print(update)
        if text == "/start":
            # response = f'سلام {update["message"]["first_name"]} عزیز! \n به سیستم خوش آمدید'
           
            await bot_api.send_message(chat_id, f'سلام {message["chat"]["first_name"]} عزیز! \n به سیستم خوش آمدید.')
            await bot_api.send_message(chat_id, 'برای شروع یکی از عملکرد های زیر رو انتخاب کنید.')
        else:
            await bot_api.send_message(chat_id, f"شما گفتید: {text}")
