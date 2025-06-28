import asyncpg
import asyncio

# لیست سؤالات
questions = [
    "نام و نام خانوادگی",
    "نام شرکت مطبوع",
    "پست سازمانی",
    "شماره همراه",
    "عنوان پیشنهاد سازمانی ",
    "حوزه مرتبط (بهره برداری - مهندی - مشترکین - مالی - منابع انسانی - فرآیندها - مدیریت) ",
    "کلمات کلیدی",
    "شرح مساله",
    "شرح نوآوری",
    "توضیحات تکمیلی ",
]

async def fetch_questions():
    conn = await asyncpg.connect("postgresql://user:1234@localhost/dbname")
    rows = await conn.fetch("SELECT * FROM questions ORDER BY order_number")
    await conn.close()
    return rows

# asyncio.run(fetch_questions())
# await fetch_questions()

