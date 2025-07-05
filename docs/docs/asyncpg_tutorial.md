# آموزش کامل asyncpg - اتصال و عملیات با PostgreSQL

## 1. مفاهیم اولیه

### asyncpg چیست؟
asyncpg یک درایور async برای PostgreSQL است که به شما امکان اتصال و اجرای کوئری‌های پایگاه داده به صورت غیرهمزمان (asynchronous) را می‌دهد.

### نصب
```bash
pip install asyncpg
```

## 2. اتصال ساده

```python
import asyncpg

async def simple_connection():
    # اتصال به پایگاه داده
    conn = await asyncpg.connect('postgresql://username:password@localhost/database_name')
    
    # اجرای یک کوئری ساده
    result = await conn.fetchrow('SELECT version()')
    print(result)
    
    # بستن اتصال
    await conn.close()

# اجرای تابع
import asyncio
asyncio.run(simple_connection())
```

**نکات مهم:**
- `await asyncpg.connect()` - اتصال به پایگاه داده
- `await conn.fetchrow()` - دریافت یک رکورد
- `await conn.close()` - بستن اتصال

## 3. انواع دستورات SELECT

### fetchrow() - دریافت یک رکورد
```python
async def get_single_user(user_id):
    conn = await asyncpg.connect('postgresql://user:pass@localhost/mydb')
    
    # دریافت یک کاربر با ID مشخص
    user = await conn.fetchrow('SELECT id, name, age FROM users WHERE id = $1', user_id)
    
    if user:
        print(f"کاربر: {user['name']}, سن: {user['age']}")
    else:
        print("کاربر یافت نشد")
    
    await conn.close()
    return user
```

### fetch() - دریافت چندین رکورد
```python
async def get_multiple_users(min_age):
    conn = await asyncpg.connect('postgresql://user:pass@localhost/mydb')
    
    # دریافت تمام کاربرانی که سن آنها بیش از min_age است
    users = await conn.fetch('SELECT id, name, age FROM users WHERE age > $1', min_age)
    
    for user in users:
        print(f"ID: {user['id']}, نام: {user['name']}, سن: {user['age']}")
    
    await conn.close()
    return users
```

### fetchval() - دریافت یک مقدار
```python
async def count_users():
    conn = await asyncpg.connect('postgresql://user:pass@localhost/mydb')
    
    # دریافت تعداد کاربران
    count = await conn.fetchval('SELECT COUNT(*) FROM users')
    print(f"تعداد کاربران: {count}")
    
    await conn.close()
    return count
```

## 4. دستورات UPDATE

### update ساده
```python
async def update_user(user_id, new_name, new_age):
    conn = await asyncpg.connect('postgresql://user:pass@localhost/mydb')
    
    # به‌روزرسانی اطلاعات کاربر
    result = await conn.execute('UPDATE users SET name = $1, age = $2 WHERE id = $3', 
                               new_name, new_age, user_id)
    
    # result شامل تعداد رکوردهای تغییر یافته است
    print(f"تعداد رکوردهای تغییر یافته: {result}")
    
    await conn.close()
    return result
```

### update شرطی
```python
async def update_users_by_condition(old_city, new_city):
    conn = await asyncpg.connect('postgresql://user:pass@localhost/mydb')
    
    # تغییر شهر تمام کاربران
    result = await conn.execute('UPDATE users SET city = $1 WHERE city = $2', 
                               new_city, old_city)
    
    print(f"{result} کاربر از {old_city} به {new_city} منتقل شدند")
    
    await conn.close()
    return result
```

## 5. استفاده از Connection Pool

### چرا Connection Pool؟
Connection Pool مجموعه‌ای از اتصالات آماده است که:
- کارایی را افزایش می‌دهد
- منابع را بهتر مدیریت می‌کند
- برای اپلیکیشن‌های production ضروری است

```python
import asyncpg

class UserDatabase:
    def __init__(self, database_url):
        self.database_url = database_url
        self.pool = None
    
    async def init_pool(self):
        """ایجاد Connection Pool"""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,    # حداقل تعداد اتصالات
            max_size=20,   # حداکثر تعداد اتصالات
        )
        print("Connection Pool ایجاد شد")
    
    async def close_pool(self):
        """بستن Connection Pool"""
        if self.pool:
            await self.pool.close()
            print("Connection Pool بسته شد")
    
    async def get_user_by_id(self, user_id):
        """دریافت کاربر با ID"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'SELECT id, name, age, email FROM users WHERE id = $1', 
                user_id
            )
    
    async def update_user_info(self, user_id, name=None, age=None, email=None):
        """به‌روزرسانی اطلاعات کاربر"""
        async with self.pool.acquire() as conn:
            # ساخت کوئری پویا
            updates = []
            params = []
            param_count = 1
            
            if name:
                updates.append(f"name = ${param_count}")
                params.append(name)
                param_count += 1
            
            if age:
                updates.append(f"age = ${param_count}")
                params.append(age)
                param_count += 1
            
            if email:
                updates.append(f"email = ${param_count}")
                params.append(email)
                param_count += 1
            
            if updates:
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ${param_count}"
                params.append(user_id)
                
                result = await conn.execute(query, *params)
                return result
            else:
                return "UPDATE 0"
    
    async def search_users(self, **filters):
        """جستجوی کاربران با فیلترهای مختلف"""
        async with self.pool.acquire() as conn:
            conditions = []
            params = []
            param_count = 1
            
            for field, value in filters.items():
                if field == 'min_age':
                    conditions.append(f"age >= ${param_count}")
                    params.append(value)
                elif field == 'max_age':
                    conditions.append(f"age <= ${param_count}")
                    params.append(value)
                elif field == 'city':
                    conditions.append(f"city = ${param_count}")
                    params.append(value)
                elif field == 'name_like':
                    conditions.append(f"name ILIKE ${param_count}")
                    params.append(f"%{value}%")
                param_count += 1
            
            query = "SELECT id, name, age, city, email FROM users"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            return await conn.fetch(query, *params)
```

## 6. مثال کاربردی کامل

```python
import asyncio
import asyncpg

async def main():
    # ایجاد instance از کلاس
    db = UserDatabase('postgresql://user:password@localhost/mydb')
    
    try:
        # ایجاد Connection Pool
        await db.init_pool()
        
        # دریافت کاربر با ID = 1
        user = await db.get_user_by_id(1)
        if user:
            print(f"کاربر یافت شد: {user['name']}")
        
        # به‌روزرسانی سن کاربر
        result = await db.update_user_info(1, age=25)
        print(f"نتیجه آپدیت: {result}")
        
        # جستجوی کاربران
        young_users = await db.search_users(min_age=18, max_age=30)
        print(f"تعداد کاربران جوان: {len(young_users)}")
        
        # جستجوی کاربران در شهر خاص
        tehran_users = await db.search_users(city='Tehran')
        for user in tehran_users:
            print(f"کاربر تهرانی: {user['name']}")
        
    finally:
        # بستن Connection Pool
        await db.close_pool()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
```

## 7. نکات مهم و بهترین practices

### 1. مدیریت خطا
```python
async def safe_database_operation():
    db = UserDatabase('postgresql://user:pass@localhost/mydb')
    
    try:
        await db.init_pool()
        
        # عملیات پایگاه داده
        user = await db.get_user_by_id(1)
        
    except asyncpg.PostgresError as e:
        print(f"خطای پایگاه داده: {e}")
    except Exception as e:
        print(f"خطای عمومی: {e}")
    finally:
        await db.close_pool()
```

### 2. استفاده از Transaction
```python
async def transfer_money(from_user_id, to_user_id, amount):
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # کسر مبلغ از حساب اول
            await conn.execute(
                'UPDATE accounts SET balance = balance - $1 WHERE user_id = $2',
                amount, from_user_id
            )
            
            # اضافه کردن مبلغ به حساب دوم
            await conn.execute(
                'UPDATE accounts SET balance = balance + $1 WHERE user_id = $2',
                amount, to_user_id
            )
```

### 3. پارامترهای امن
```python
# ✅ درست - استفاده از پارامتر
user_id = 1
result = await conn.fetchrow('SELECT * FROM users WHERE id = $1', user_id)

# ❌ غلط - خطر SQL Injection
user_id = 1
result = await conn.fetchrow(f'SELECT * FROM users WHERE id = {user_id}')
```

## 8. خلاصه دستورات مهم

| دستور | کاربرد |
|--------|---------|
| `fetchrow()` | دریافت یک رکورد |
| `fetch()` | دریافت چندین رکورد |
| `fetchval()` | دریافت یک مقدار |
| `execute()` | اجرای UPDATE/INSERT/DELETE |
| `$1, $2, $3` | پارامترهای امن |
| `async with pool.acquire()` | دریافت اتصال از Pool |
| `async with conn.transaction()` | استفاده از Transaction |

این ساختار به شما کمک می‌کند تا به راحتی با asyncpg کار کنید و عملیات پایگاه داده را به صورت ایمن و کارآمد انجام دهید.