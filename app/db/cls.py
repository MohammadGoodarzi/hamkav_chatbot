import asyncpg
from typing import Dict, List, Any, Union, Optional
import logging

# تنظیم لاگ برای نوشتن در فایل
logging.basicConfig(
    filename='app/logs/db_errors.log',          # نام فایل لاگ
    level=logging.ERROR,               # فقط خطاها ثبت بشن
    format='%(asctime)s - %(levelname)s - %(message)s',  # فرمت لاگ
    datefmt='%Y-%m-%d %H:%M:%S'        # فرمت تاریخ و زمان
)



# لاگ تنظیم شده در بالا قرار دارد

class Database:
    """
    sample 1 ::
    
    async with Database() as db:
        # استفاده از کانفیگ پیش‌فرض
        results = await db.pool.fetch("SELECT * FROM users")
        
      
    sample 2 ::
        
    custom_config = {
    "user": "admin",
    "password": "secure_pass",
    "database": "production_db",
    "host": "db.server.com"
    }

    async with Database(custom_config) as db:
        # استفاده از کانفیگ سفارشی
        results = await db.pool.fetch("SELECT * FROM orders")
        
    """
    
    
    # متغیر کلاس - فقط یک نمونه از کلاس می‌تونه وجود داشته باشه
    _instance = None
    _pool = None
    _default_config = {
        "user": "postgres",
        "password": "1234",
        "database": "social_chat_bot",
        "host": "localhost"
    }

    def __new__(cls, config: Optional[Dict[str, Any]] = None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._config = config if config else cls._default_config
        return cls._instance
    
    def _initialize(self, config: Optional[Dict[str, Any]]):
        """
        متد مقداردهی اولیه - فقط یک بار صدا زده می‌شه
        """
        self.pool = None  # متغیر برای نگهداری connection pool
        
        # اگر کانفیگ ارسال شده از آن استفاده کن، در غیر اینصورت از پیش‌فرض
        self.config = config if config else self._default_config
        
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        

    async def connect(self):
        """ایجاد connection pool"""
        if self._pool is None:
            self._pool = await asyncpg.create_pool(**self._config)
        return self

    async def close(self):
        """بستن connection pool"""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute_select(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            if not self.pool:
                logging.error("Database pool is not initialized.")
                # return []
                return None

            async with self.pool.acquire() as conn:
                try:
                    stmt = await conn.prepare(query)
                    params_list = list(params.values()) if params else []
                    records = await stmt.fetch(*params_list)
                    return [dict(record) for record in records]
                except Exception as e:
                    print(e)
                    logging.error(f"Query Execution Error: {e}")
                    return []
        except Exception as e:
            print(e)
            logging.error(f"Unexpected Error: {e}")
            return []
    
    async def execute_update(
        self,
        query: str,
        params: Dict[str, Any] = None,
        returning: bool = False
        ) -> Union[int, List[Dict[str, Any]]]:
        """
        اجرای کوئری UPDATE دلخواه با پارامترهای دیکشنری
        
        Args:
            query: متن کامل کوئری UPDATE با placeholders به صورت $1, $2, ...
            params: دیکشنری پارامترها {'param1': value1, 'param2': value2}
            returning: آیا نتیجه کوئری RETURNING باید برگردد؟
        
        Returns:
            - اگر returning=False: تعداد رکوردهای affected (int)
            - اگر returning=True: لیست دیکشنری‌های رکوردهای به‌روز شده
        
        Raises:
            RuntimeError: اگر خطایی در اجرا رخ دهد
        """
        if not self._is_connected:
            raise RuntimeError("اتصال به دیتابیس برقرار نشده است")

        try:
            async with self.pool.acquire() as conn:
                stmt = await conn.prepare(query)
                
                if params:
                    # تبدیل دیکشنری به لیست با ترتیب پارامترهای کوئری
                    param_names = stmt.get_parameters()
                    params_list = [params.get(name) for name in param_names]
                    
                    if returning:
                        records = await stmt.fetch(*params_list)
                        return [dict(record) for record in records]
                    else:
                        result = await stmt.execute(*params_list)
                        return int(result.split()[-1])
                else:
                    if returning:
                        records = await conn.fetch(query)
                        return [dict(record) for record in records]
                    else:
                        result = await conn.execute(query)
                        return int(result.split()[-1])
                        
        except asyncpg.PostgresError as e:
            # raise RuntimeError(f"خطای دیتابیس در اجرای UPDATE: {str(e)}")
            print("error in log file!")
            logging.error(f" خطای دیتابیس در اجرای UPDATE: {e}")

    async def execute_insert(self, query: str, params: Dict[str, Any] = None, id_column: str = "id") -> Any:
        """اجرای کوئری INSERT و برگرداندن ID"""
        if self._pool is None:
            raise RuntimeError("Connection pool is not initialized. Call connect() first.")

        try:
            # print(query)
            async with self._pool.acquire() as conn:
                # اضافه کردن RETURNING اگر وجود ندارد
                if f"RETURNING {id_column}" not in query.upper():
                    query = f"{query.rstrip(';')} RETURNING {id_column};"

                if params:
                    stmt = await conn.prepare(query)
                    param_names = stmt.get_parameters()
                    params_list = [params.get(name) for name in param_names]
                    return await stmt.fetchval(*params_list)
                return await conn.fetchval(query)

        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise RuntimeError(f"خطا در اجرای INSERT: {str(e)}")