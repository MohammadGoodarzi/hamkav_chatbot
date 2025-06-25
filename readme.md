# HAMKAV SOCIAL MEDIA CHAT BOT

## STRUCTURE

```
app/
├── main.py              # FastAPI اپ
├── bot/
│   ├── __init__.py
│   ├── api.py          # کد ارسال درخواست به API پیام‌رسان (تغییر پذیر)
│   ├── handlers.py     # منطق پاسخ به پیام‌ها
│   └── core.py         # مدیریت ربات (Polling/Webhook)
├── config.py           # پیکربندی
```


## INSTALLING
### install requrements in python
pip install -r requirements.txt

### .env files
create a .env file in root of project that have below items:

BOT_TOKEN={your api key}
API_BASE_URL=https://tapi.bale.ai  # یا https://api.telegram.org
RUNNING_MODE=polling # مقدارهای ممکن: webhook یا polling
WEBHOOK_URL=https://yourdomain.com/webhook




## RUNNING APP
uvicorn app.main:app --reload

