import asyncpg
from typing import Dict, List, Any, Union
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
    def __init__(self, connection_params: Dict[str, Any]):
        self.connection_params = connection_params
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(**self.connection_params)
        except Exception as e:
            logging.error(f"Connection Error: {e}")

    async def close(self):
        try:
            if self.pool:
                await self.pool.close()
        except Exception as e:
            logging.error(f"Close Error: {e}")

    async def execute_select(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            if not self.pool:
                logging.error("Database pool is not initialized.")
                return []

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
            logging.error(f" خطای دیتابیس در اجرای UPDATE: {e}")
        
        
        
    
    
    
        
        