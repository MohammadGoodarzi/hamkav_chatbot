
from cls import Database

async def main():
    # نمونه‌سازی با تنظیمات خاص
    db = Database({
        'user': 'postgres',
        'password': '1234',
        'database': 'social_chat_bot',
        'host': 'localhost'
    })
    
    await db.connect()
    
    try:
        # results = await db.execute_select(
        #     "SELECT * FROM users WHERE age > $1",
        #     {'age': 20}
        # )
        results = await db.execute_select(
            "SELECT * FROM dialog.question2",{}
        )
        print(results)
    finally:
        await db.close()

# اجرا
import asyncio  # noqa: E402
asyncio.run(main())