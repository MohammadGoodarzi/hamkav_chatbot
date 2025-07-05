# راهنمای Type Hints در Python

## مقدمه
Type Hints راهی برای مشخص کردن نوع متغیرها، پارامترها و مقادیر بازگشتی در Python است. این قابلیت کد را خواناتر و قابل نگهداری‌تر می‌کند.

## چرا Type Hints مهم است؟

### بدون Type Hints:
```python
def process_data(data, config):
    # نمی‌دانیم data چه نوعی است
    # نمی‌دانیم config چه نوعی است
    # نمی‌دانیم چه چیزی برمی‌گرداند
    result = data * config.get('multiplier', 1)
    return result
```

### با Type Hints:
```python
from typing import Dict, Any, Union

def process_data(data: Union[int, float], config: Dict[str, Any]) -> Union[int, float]:
    # واضح است که data عدد است
    # واضح است که config دیکشنری است
    # واضح است که عدد برمی‌گرداند
    result = data * config.get('multiplier', 1)
    return result
```

## انواع Type Hints

### 1. انواع پایه
```python
# انواع ساده
name: str = "علی"
age: int = 25
height: float = 1.75
is_student: bool = True

# تابع با Type Hints
def greet(name: str) -> str:
    return f"سلام {name}"

def calculate_area(width: float, height: float) -> float:
    return width * height
```

### 2. Collections (مجموعه‌ها)
```python
from typing import List, Dict, Tuple, Set

# لیست
numbers: List[int] = [1, 2, 3, 4, 5]
names: List[str] = ["علی", "فاطمه", "محمد"]

# دیکشنری
user_data: Dict[str, Any] = {
    "name": "علی",
    "age": 25,
    "scores": [85, 90, 78]
}

# تاپل
coordinates: Tuple[float, float] = (10.5, 20.3)
rgb_color: Tuple[int, int, int] = (255, 128, 0)

# مجموعه
unique_ids: Set[int] = {1, 2, 3, 4, 5}
```

### 3. Optional و Union
```python
from typing import Optional, Union

# Optional - می‌تواند None باشد
def find_user(user_id: int) -> Optional[str]:
    # ممکن است کاربر پیدا نشود
    if user_id > 0:
        return f"کاربر {user_id}"
    return None

# Union - می‌تواند چند نوع مختلف باشد
def process_id(user_id: Union[int, str]) -> str:
    if isinstance(user_id, int):
        return f"ID: {user_id}"
    return f"Username: {user_id}"
```

## Type Hints در کد شما

### تحلیل کد Database:
```python
from typing import Dict, Any, List, Union, Optional

class Database:
    def __init__(self, connection_params: Dict[str, Any]):
        # Dict[str, Any] = دیکشنری با کلید string و مقدار هر نوعی
        self.connection_params = connection_params
        self.pool = None

    async def execute_select(
        self, 
        query: str, 
        params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        # پارامترها:
        # query: str = رشته کوئری
        # params: Dict[str, Any] = دیکشنری پارامترها (اختیاری)
        # برمی‌گرداند: List[Dict[str, Any]] = لیست از دیکشنری‌ها
        
        # ...کد اجرای کوئری...
        return [dict(record) for record in records]

    async def execute_update(
        self,
        query: str,
        params: Dict[str, Any] = None,
        returning: bool = False
    ) -> Union[int, List[Dict[str, Any]]]:
        # Union[int, List[Dict[str, Any]]] = 
        # یا عدد (تعداد رکوردهای affected) یا لیست دیکشنری
        
        if returning:
            return [dict(record) for record in records]  # List[Dict[str, Any]]
        else:
            return affected_rows_count  # int
```

## Type Hints پیشرفته

### 1. Generic Types
```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self):
        self.items: List[T] = []
    
    def add(self, item: T) -> None:
        self.items.append(item)
    
    def get_all(self) -> List[T]:
        return self.items

# استفاده
user_repo = Repository[User]()
product_repo = Repository[Product]()
```

### 2. Callable
```python
from typing import Callable

def run_callback(callback: Callable[[int, str], bool]) -> None:
    # callback تابعی است که int و str می‌گیرد و bool برمی‌گرداند
    result = callback(42, "test")
    print(result)

# استفاده
def my_callback(num: int, text: str) -> bool:
    return num > 0 and len(text) > 0

run_callback(my_callback)
```

### 3. Protocol
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("رسم دایره")

class Square:
    def draw(self) -> None:
        print("رسم مربع")

def render_shape(shape: Drawable) -> None:
    shape.draw()

# هر کلاسی که draw دارد، Drawable محسوب می‌شود
render_shape(Circle())
render_shape(Square())
```

## در کلاس‌ها

### نوع‌دهی پراپرتی‌ها و متدها:
```python
from typing import Optional, List, Dict, Any

class User:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age
        self.email: Optional[str] = None  # ممکن است تنظیم نشود
        self.scores: List[float] = []     # لیست نمرات
    
    def add_score(self, score: float) -> None:
        self.scores.append(score)
    
    def get_average_score(self) -> Optional[float]:
        if not self.scores:
            return None
        return sum(self.scores) / len(self.scores)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'scores': self.scores
        }
```

## مزایای Type Hints

### 1. خوانایی کد
```python
# واضح است که چه انتظاری داریم
def calculate_tax(income: float, tax_rate: float) -> float:
    return income * tax_rate

# مبهم است
def calculate_tax(income, tax_rate):
    return income * tax_rate
```

### 2. IDE Support
- **AutoComplete**: IDE می‌تواند متدهای مناسب را پیشنهاد دهد
- **Error Detection**: خطاهای نوع داده قبل از اجرا شناسایی می‌شوند
- **Refactoring**: تغییرات امن‌تر

### 3. Documentation
```python
def process_user_data(
    user_id: int,
    personal_info: Dict[str, str],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    پردازش داده‌های کاربر
    
    Args:
        user_id: شناسه کاربر (عدد)
        personal_info: اطلاعات شخصی (دیکشنری)
        preferences: تنظیمات (اختیاری)
    
    Returns:
        داده‌های پردازش شده
    """
    # ...
```

## ابزارها

### 1. mypy - Type Checker
```bash
pip install mypy
mypy my_code.py
```

### 2. استفاده در IDE
- **PyCharm**: پشتیبانی کامل
- **VS Code**: با extension Python
- **Sublime**: با plugin‌های مناسب

## نکات مهم

### 1. Type Hints اجباری نیست
```python
# هر دو معتبر هستند
def func1(x: int) -> str:
    return str(x)

def func2(x):
    return str(x)
```

### 2. Runtime Effect ندارد
```python
# این کد اجرا می‌شود اما نوع اشتباه است
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")  # خطای نوع اما اجرا می‌شود
```

### 3. Import کردن Types
```python
# Python 3.9+
from typing import List, Dict, Optional

# Python 3.9+ - Built-in
def process_data(data: list[dict[str, str]]) -> dict[str, int]:
    pass
```

## مثال کاربردی کامل

### کلاس Database با Type Hints کامل:
```python
from typing import Dict, Any, List, Optional, Union
import asyncpg
import logging

class Database:
    def __init__(self, connection_params: Dict[str, Any]) -> None:
        self.connection_params: Dict[str, Any] = connection_params
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(**self.connection_params)
        except Exception as e:
            logging.error(f"Connection Error: {e}")
            raise
    
    async def execute_select(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as conn:
            stmt = await conn.prepare(query)
            params_list = list(params.values()) if params else []
            records = await stmt.fetch(*params_list)
            return [dict(record) for record in records]
    
    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
```

## خلاصه
- **Type Hints** خوانایی و نگهداری کد را بهبود می‌بخشد
- **IDE Support** بهتر و تشخیص خطا
- **Documentation** طبیعی کد
- **اجباری نیست** اما توصیه می‌شود
- **mypy** برای بررسی نوع داده‌ها