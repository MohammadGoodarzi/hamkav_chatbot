# آموزش برنامه‌نویسی ناهمزمان (Async Programming) در پایتون

## معرفی
برنامه‌نویسی ناهمزمان (Asynchronous Programming) یکی از مهم‌ترین تکنیک‌های مدرن در پایتون است که به شما اجازه می‌دهد چندین کار را به طور همزمان انجام دهید بدون اینکه برنامه شما منتظر بماند.

## مفاهیم کلیدی

### 1. async/await

#### `async def` - تعریف تابع ناهمزمان
```python
async def my_async_function():
    print("این یک تابع ناهمزمان است")
    # کدهای دیگر...
```

**توضیح:**
- هر تابعی که با `async def` تعریف می‌شود، یک Coroutine یا همان کوروتین محسوب می‌شود
- این توابع نمی‌توانند مستقیماً صدا زده شوند، بلکه باید با `await` فراخوانی شوند

#### `await` - انتظار برای اتمام کار
```python
async def fetch_data():
    # انتظار برای اتمام عملیات
    result = await some_async_operation()
    return result
```

**توضیح:**
- `await` به برنامه می‌گوید که در این نقطه منتظر بماند تا عملیات کامل شود
- در طول انتظار، برنامه می‌تواند کارهای دیگر را انجام دهد

### 2. Context Manager در محیط ناهمزمان

#### `async with` - مدیریت منابع
```python
async with self.pool.acquire() as conn:
    # استفاده از اتصال
    result = await conn.execute(query)
# اتصال به طور خودکار بسته می‌شود
```

**مزایا:**
- اطمینان از بسته شدن منابع (مثل اتصالات دیتابیس)
- مدیریت خودکار خطاها
- کد تمیز و قابل خواندن

### 3. مثال کاربردی - اتصال به دیتابیس

```python
import asyncio
import asyncpg

class Database:
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.pool = None
    
    async def connect(self):
        """ایجاد اتصال به دیتابیس"""
        try:
            self.pool = await asyncpg.create_pool(**self.connection_params)
            print("اتصال برقرار شد")
        except Exception as e:
            print(f"خطا در اتصال: {e}")
    
    async def fetch_users(self):
        """دریافت کاربران از دیتابیس"""
        async with self.pool.acquire() as conn:
            records = await conn.fetch("SELECT * FROM users")
            return [dict(record) for record in records]

# استفاده
async def main():
    db = Database({'host': 'localhost', 'database': 'mydb'})
    await db.connect()
    
    users = await db.fetch_users()
    print(f"تعداد کاربران: {len(users)}")

# اجرای برنامه
asyncio.run(main())
```

## چرا از برنامه‌نویسی ناهمزمان استفاده کنیم؟

### 1. کارایی بهتر
```python
# روش سنتی (همزمان)
def slow_function():
    time.sleep(2)  # برنامه کاملاً متوقف می‌شود
    return "نتیجه"

# روش ناهمزمان
async def fast_function():
    await asyncio.sleep(2)  # برنامه کارهای دیگر را می‌تواند انجام دهد
    return "نتیجه"
```

### 2. مدیریت بهتر I/O Operations
- عملیات شبکه (Network requests)
- خواندن/نوشتن فایل
- عملیات دیتابیس

### 3. مثال مقایسه‌ای
```python
import asyncio
import time

# روش همزمان
def sync_task():
    time.sleep(1)
    return "کامل شد"

def run_sync_tasks():
    start = time.time()
    results = []
    
    for i in range(5):
        results.append(sync_task())
    
    end = time.time()
    print(f"زمان کل (همزمان): {end - start:.2f} ثانیه")  # ~5 ثانیه

# روش ناهمزمان
async def async_task():
    await asyncio.sleep(1)
    return "کامل شد"

async def run_async_tasks():
    start = time.time()
    
    # همه کارها به طور همزمان شروع می‌شوند
    tasks = [async_task() for _ in range(5)]
    results = await asyncio.gather(*tasks)
    
    end = time.time()
    print(f"زمان کل (ناهمزمان): {end - start:.2f} ثانیه")  # ~1 ثانیه
```

## نکات مهم

### 1. خطاهای متداول
```python
# اشتباه: فراموش کردن await
async def wrong_way():
    result = async_function()  # غلط!
    return result

# صحیح: استفاده از await
async def correct_way():
    result = await async_function()  # درست!
    return result
```

### 2. مدیریت خطا
```python
async def safe_operation():
    try:
        result = await risky_async_operation()
        return result
    except Exception as e:
        print(f"خطا رخ داد: {e}")
        return None
```

### 3. تایم‌اوت (Timeout)
```python
async def operation_with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_async_operation(), 
            timeout=5.0  # 5 ثانیه تایم‌اوت
        )
        return result
    except asyncio.TimeoutError:
        print("عملیات خیلی طول کشید!")
        return None
```

## خلاصه
برنامه‌نویسی ناهمزمان برای کارهایی که شامل انتظار است (مثل عملیات دیتابیس، درخواست‌های شبکه) بسیار مفید است. با استفاده از `async/await` می‌توانید:

- کارایی برنامه را بهبود دهید
- منابع سیستم را بهتر مدیریت کنید
- تجربه کاربری بهتری ارائه دهید

یادگیری این مفاهیم برای توسعه‌دهندگان مدرن پایتون ضروری است.