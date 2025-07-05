import asyncpg
import asyncio
from typing import List, Dict, Any, Optional, Union


class DatabaseManager:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None

    async def init_pool(self):
        """ایجاد Connection Pool"""
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=5,
            max_size=20,
        )
        print("Connection Pool ایجاد شد")

    async def close_pool(self):
        """بستن Connection Pool"""
        if self.pool:
            await self.pool.close()
            print("Connection Pool بسته شد")

    async def execute_select(self,
                             query: str,
                             params: Optional[Union[tuple, list]] = None,
                             fetch_type: str = 'fetch') -> Union[List[Dict], Dict, Any]:
        """
        تابع کلی برای اجرای کوئری SELECT

        Args:
            query: کوئری SQL
            params: پارامترهای کوئری (اختیاری)
            fetch_type: نوع دریافت داده ('fetch', 'fetchrow', 'fetchval')

        Returns:
            نتیجه کوئری بر اساس fetch_type
        """
        if not self.pool:
            raise Exception(
                "Connection Pool ایجاد نشده است. ابتدا init_pool() را فراخوانی کنید.")

        try:
            async with self.pool.acquire() as conn:
                if params:
                    # اگر پارامتر داریم
                    if fetch_type == 'fetch':
                        result = await conn.fetch(query, *params)
                        return [dict(row) for row in result]
                    elif fetch_type == 'fetchrow':
                        result = await conn.fetchrow(query, *params)
                        return dict(result) if result else None
                    elif fetch_type == 'fetchval':
                        result = await conn.fetchval(query, *params)
                        return result
                else:
                    # اگر پارامتر نداریم
                    if fetch_type == 'fetch':
                        result = await conn.fetch(query)
                        return [dict(row) for row in result]
                    elif fetch_type == 'fetchrow':
                        result = await conn.fetchrow(query)
                        return dict(result) if result else None
                    elif fetch_type == 'fetchval':
                        result = await conn.fetchval(query)
                        return result

        except asyncpg.PostgresError as e:
            print(f"خطای پایگاه داده: {e}")
            raise
        except Exception as e:
            print(f"خطای عمومی: {e}")
            raise

    # تابع‌های کمکی برای راحتی کار
    async def select_many(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """دریافت چندین رکورد"""
        return await self.execute_select(query, params, 'fetch')

    async def select_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict]:
        """دریافت یک رکورد"""
        return await self.execute_select(query, params, 'fetchrow')

    async def select_value(self, query: str, params: Optional[tuple] = None) -> Any:
        """دریافت یک مقدار"""
        return await self.execute_select(query, params, 'fetchval')


# مثال‌های کاربردی
async def main():
    # ایجاد instance از کلاس
    db = DatabaseManager('postgresql://user:password@localhost/mydb')

    try:
        # ایجاد Connection Pool
        await db.init_pool()

        # مثال 1: دریافت تمام کاربران
        print("=== مثال 1: دریافت تمام کاربران ===")
        users = await db.select_many("SELECT id, name, age FROM users")
        for user in users:
            print(f"ID: {user['id']}, نام: {user['name']}, سن: {user['age']}")

        # مثال 2: دریافت کاربر با ID خاص
        print("\n=== مثال 2: دریافت کاربر با ID خاص ===")
        user = await db.select_one("SELECT * FROM users WHERE id = $1", (1,))
        if user:
            print(f"کاربر یافت شد: {user}")
        else:
            print("کاربر یافت نشد")

        # مثال 3: دریافت کاربران با سن بیشتر از مقدار خاص
        print("\n=== مثال 3: کاربران با سن بیشتر از 25 ===")
        older_users = await db.select_many(
            "SELECT name, age FROM users WHERE age > $1 ORDER BY age",
            (25,)
        )
        for user in older_users:
            print(f"نام: {user['name']}, سن: {user['age']}")

        # مثال 4: دریافت تعداد کاربران
        print("\n=== مثال 4: تعداد کاربران ===")
        count = await db.select_value("SELECT COUNT(*) FROM users")
        print(f"تعداد کل کاربران: {count}")

        # مثال 5: جستجوی پیشرفته با چندین پارامتر
        print("\n=== مثال 5: جستجوی پیشرفته ===")
        advanced_search = await db.select_many(
            """
            SELECT id, name, age, city 
            FROM users 
            WHERE age BETWEEN $1 AND $2 
            AND city = $3 
            ORDER BY age DESC
            """,
            (20, 40, 'Tehran')
        )
        for user in advanced_search:
            print(
                f"ID: {user['id']}, نام: {user['name']}, سن: {user['age']}, شهر: {user['city']}")

        # مثال 6: استفاده از LIKE برای جستجوی نام
        print("\n=== مثال 6: جستجوی نام با LIKE ===")
        name_search = await db.select_many(
            "SELECT id, name FROM users WHERE name ILIKE $1",
            ('%احمد%',)
        )
        for user in name_search:
            print(f"ID: {user['id']}, نام: {user['name']}")

        # مثال 7: دریافت میانگین سن
        print("\n=== مثال 7: میانگین سن کاربران ===")
        avg_age = await db.select_value("SELECT AVG(age) FROM users")
        print(f"میانگین سن: {avg_age:.2f}")

        # مثال 8: کوئری پیچیده با JOIN
        print("\n=== مثال 8: کوئری با JOIN ===")
        user_orders = await db.select_many(
            """
            SELECT u.name, u.email, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.age > $1
            GROUP BY u.id, u.name, u.email
            HAVING COUNT(o.id) > $2
            ORDER BY order_count DESC
            """,
            (18, 0)
        )
        for record in user_orders:
            print(
                f"نام: {record['name']}, ایمیل: {record['email']}, تعداد سفارش: {record['order_count']}")

    except Exception as e:
        print(f"خطا در اجرای برنامه: {e}")

    finally:
        # بستن Connection Pool
        await db.close_pool()


# تابع‌های standalone برای استفاده آسان‌تر
async def simple_select(connection_string: str, query: str, params: Optional[tuple] = None):
    """تابع ساده برای اجرای کوئری SELECT بدون نیاز به کلاس"""
    conn = await asyncpg.connect(connection_string)
    try:
        if params:
            result = await conn.fetch(query, *params)
        else:
            result = await conn.fetch(query)
        return [dict(row) for row in result]
    finally:
        await conn.close()


# مثال استفاده از تابع ساده
async def simple_example():
    print("=== مثال استفاده از تابع ساده ===")

    # دریافت کاربران با سن بیشتر از 25
    users = await simple_select(
        'postgresql://user:password@localhost/mydb',
        'SELECT name, age FROM users WHERE age > $1',
        (25,)
    )

    for user in users:
        print(f"نام: {user['name']}, سن: {user['age']}")


if __name__ == "__main__":
    # اجرای مثال کامل
    asyncio.run(main())

    # اجرای مثال ساده
    # asyncio.run(simple_example())
