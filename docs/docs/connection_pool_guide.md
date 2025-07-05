# راهنمای Connection Pool در دیتابیس

## مقدمه
Connection Pool مجموعه‌ای از اتصالات از پیش تعریف شده به دیتابیس است که برای بهبود کارایی و مدیریت منابع استفاده می‌شود.

## مشکل بدون Connection Pool

### روش سنتی (بدون Pool):
```python
import asyncpg

# هر بار اتصال جدید
async def get_user(user_id):
    conn = await asyncpg.connect("postgresql://...")  # ایجاد اتصال
    result = await conn.fetch("SELECT * FROM users WHERE id = $1", user_id)
    await conn.close()  # بستن اتصال
    return result
```

### مشکلات روش سنتی:
- **کندی**: هر بار باید اتصال جدید ایجاد کرد
- **هزینه بالا**: ایجاد و بستن اتصال منابع زیادی مصرف می‌کند
- **محدودیت**: تعداد اتصالات همزمان محدود است
- **ناکارآمدی**: در ترافیک بالا عملکرد ضعیف دارد

## راه‌حل: Connection Pool

### مفهوم Pool:
```python
# ایجاد Pool
pool = await asyncpg.create_pool(
    host="localhost",
    port=5432,
    user="username",
    password="password",
    database="mydb",
    min_size=5,      # حداقل اتصال
    max_size=20,     # حداکثر اتصال
    command_timeout=60
)

# استفاده از Pool
async with pool.acquire() as conn:
    result = await conn.fetch("SELECT * FROM users")
# اتصال به طور خودکار به Pool برمی‌گردد
```

## مزایای Connection Pool

### 1. بهبود کارایی
- اتصالات از پیش آماده هستند
- عدم نیاز به ایجاد اتصال جدید هر بار
- سرعت بالاتر در اجرای کوئری‌ها

### 2. مدیریت منابع
- کنترل تعداد اتصالات همزمان
- جلوگیری از اتمام اتصالات دیتابیس
- بهینه‌سازی مصرف memory

### 3. قابلیت اطمینان
- مدیریت خودکار اتصالات خراب
- بازیابی اتصال در صورت قطع شدن
- تنظیمات timeout

## پیاده‌سازی در کد شما

### کلاس Database با Pool:
```python
class Database:
    def __init__(self, connection_params: Dict[str, Any]):
        self.connection_params = connection_params
        self.pool = None

    async def connect(self):
        """ایجاد Connection Pool"""
        try:
            self.pool = await asyncpg.create_pool(**self.connection_params)
            print("Connection Pool ایجاد شد")
        except Exception as e:
            logging.error(f"خطا در ایجاد Pool: {e}")

    async def execute_select(self, query: str, params: Dict[str, Any] = None):
        """استفاده از Pool برای اجرای کوئری"""
        if not self.pool:
            logging.error("Pool هنوز ایجاد نشده")
            return []

        # گرفتن اتصال از Pool
        async with self.pool.acquire() as conn:
            stmt = await conn.prepare(query)
            records = await stmt.fetch(*params_list)
            return [dict(record) for record in records]
        # اتصال خودکار به Pool برمی‌گردد
```

## تنظیمات مهم Pool

### پارامترهای کلیدی:
```python
pool = await asyncpg.create_pool(
    # اتصال دیتابیس
    host="localhost",
    port=5432,
    user="username",
    password="password",
    database="mydb",
    
    # تنظیمات Pool
    min_size=5,              # حداقل اتصال در Pool
    max_size=20,             # حداکثر اتصال در Pool
    max_queries=50000,       # حداکثر کوئری در هر اتصال
    max_inactive_connection_lifetime=300,  # مدت زندگی اتصال غیرفعال
    
    # Timeout ها
    command_timeout=60,      # مهلت اجرای کوئری
    server_settings={
        'application_name': 'my_app',
        'timezone': 'UTC'
    }
)
```

### توضیح پارامترها:
- **min_size**: تعداد اتصالات اولیه که همیشه باز هستند
- **max_size**: حداکثر تعداد اتصالات موازی
- **max_queries**: بعد از این تعداد کوئری، اتصال بازیابی می‌شود
- **command_timeout**: مهلت انتظار برای اجرای کوئری

## بهترین practices

### 1. Context Manager
```python
# درست ✅
async with pool.acquire() as conn:
    result = await conn.fetch("SELECT ...")
# اتصال خودکار آزاد می‌شود

# غلط ❌
conn = await pool.acquire()
result = await conn.fetch("SELECT ...")
# اتصال آزاد نمی‌شود!
```

### 2. مدیریت خطا
```python
async def safe_query(pool, query):
    try:
        async with pool.acquire() as conn:
            return await conn.fetch(query)
    except asyncpg.PostgresError as e:
        logging.error(f"خطای دیتابیس: {e}")
        return []
    except Exception as e:
        logging.error(f"خطای غیرمنتظره: {e}")
        return []
```

### 3. بستن Pool
```python
async def cleanup(pool):
    if pool:
        await pool.close()
        print("Pool بسته شد")
```

## مثال کاربردی

### استفاده در برنامه وب:
```python
import asyncio
from typing import Dict, Any

class DatabaseManager:
    def __init__(self):
        self.pool = None
    
    async def startup(self):
        """راه‌اندازی Pool در شروع برنامه"""
        self.pool = await asyncpg.create_pool(
            host="localhost",
            database="myapp",
            user="user",
            password="pass",
            min_size=10,
            max_size=100
        )
        print("Database Pool آماده است")
    
    async def shutdown(self):
        """بستن Pool در پایان برنامه"""
        if self.pool:
            await self.pool.close()
            print("Database Pool بسته شد")
    
    async def get_users(self, limit: int = 10):
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                "SELECT * FROM users LIMIT $1", 
                limit
            )

# استفاده
db_manager = DatabaseManager()
await db_manager.startup()

# اجرای کوئری‌ها
users = await db_manager.get_users(50)

# پایان برنامه
await db_manager.shutdown()
```

## خلاصه
- **Connection Pool** مجموعه اتصالات از پیش آماده
- **بهبود کارایی** و **مدیریت منابع**
- **Context Manager** برای استفاده ایمن
- **تنظیمات مناسب** برای کارایی بهتر
- **ضروری** برای برنامه‌های production