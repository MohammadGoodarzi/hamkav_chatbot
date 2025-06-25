from app.bot.api import BotAPI
from telegram import ReplyKeyboardMarkup
import json
from .data_layer import questions

bot_api = BotAPI()

# حافظه موقت وضعیت کاربران
user_states = {}  # chat_id: {"step": int, "answers": list[str]}

async def handle_update(update: dict):
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    first_name = message["chat"].get("first_name", "کاربر")

    user = user_states.get(chat_id)

    keyboard_markup = {
        "keyboard": [["تکمیل فرم"]],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    inline_markup = {
    "inline_keyboard": [
        [
            {"text": "📝 تکمیل فرم", "callback_data": "start_form"}
        ]
    ]
    }
    
    # وقتی کاربر /start می‌فرسته
    if text == "/start":
        await bot_api.send_message(chat_id, f'سلام {first_name} عزیز! 👋\nبه ربات خوش آمدید.')
        # نمایش دکمه "تکمیل فرم"
        keyboard = ReplyKeyboardMarkup([["تکمیل فرم"]], resize_keyboard=True)
        # keyboard = ReplyKeyboardMarkup([["تکمیل فرم"]], resize_keyboard=True)
        # await bot_api.send_message(chat_id, "برای شروع، روی دکمه‌ی زیر کلیک کن:", reply_markup=keyboard)
        await bot_api.send_message(
        chat_id,
        "برای شروع، روی دکمه‌ی تکمیل فرم کلیک کن:",
        reply_markup=keyboard_markup
        )
        
        return

    # اگر فرم هنوز شروع نشده و کاربر "تکمیل فرم" زده
    if text == "تکمیل فرم" and not user:
        user_states[chat_id] = {"step": 0, "answers": []}
        await bot_api.send_message(chat_id, "باشه، شروع کنیم ✍️")
        await bot_api.send_message(chat_id, questions[0])
        return

    # اگر کاربر در حال پر کردن فرم است
    if user:
        step = user["step"]
        answers = user["answers"]

        # ذخیره پاسخ
        if step < len(questions):
            answers.append(text)
            step += 1
            user["step"] = step
            user["answers"] = answers

        if step < len(questions):
            await bot_api.send_message(chat_id, questions[step])
        else:
            result = {f"سوال {i+1}": ans for i, ans in enumerate(answers)}
            result_json = json.dumps(result, ensure_ascii=False, indent=2)
            await bot_api.send_message(chat_id, "✅ ممنون! همه پاسخ‌ها ثبت شد.")
            await bot_api.send_message(chat_id, f"{result_json}")
            user_states.pop(chat_id)
        return

    # هر پیام دیگه:
    await bot_api.send_message(chat_id, "برای شروع لطفاً /start را ارسال کن یا روی دکمه‌ی «تکمیل فرم» کلیک کن.")
