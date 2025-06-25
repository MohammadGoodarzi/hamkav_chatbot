app/
├── main.py           # FastAPI اپ
├── bot/
│   ├── __init__.py
│   ├── api.py        # کد ارسال درخواست به API پیام‌رسان (تغییر پذیر)
│   ├── handlers.py   # منطق پاسخ به پیام‌ها
│   └── core.py       # مدیریت ربات (Polling/Webhook)
├── config.py         # پیکربندی


pip install -r requirements.txt
uvicorn app.main:app --reload

