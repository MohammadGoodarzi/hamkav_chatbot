# آموزش کامل کلاس‌نویسی در پایتون

## مقدمه
کلاس‌ها در پایتون قالب‌هایی هستند که می‌توانیم از آنها شی (object) بسازیم. در این آموزش با مفاهیم پیشرفته کلاس‌نویسی آشنا می‌شویم.

## 1. مفهوم کلاس و شی

```python
class Person:
    def __init__(self, name):
        self.name = name

# ساختن شی از کلاس
person1 = Person("احمد")
person2 = Person("فاطمه")
print(person1.name)  # احمد
print(person2.name)  # فاطمه
```

هر بار که `Person()` می‌نویسیم، یک شی جدید ساخته می‌شود.

## 2. متغیرهای کلاس (Class Variables)

```python
class Student:
    # متغیر کلاس - برای همه نمونه‌ها مشترک است
    school_name = "دانشگاه تهران"
    
    def __init__(self, name):
        # متغیر نمونه - برای هر شی جداگانه است
        self.name = name

student1 = Student("علی")
student2 = Student("مریم")

print(student1.school_name)  # دانشگاه تهران
print(student2.school_name)  # دانشگاه تهران

# تغییر متغیر کلاس
Student.school_name = "دانشگاه شریف"
print(student1.school_name)  # دانشگاه شریف
print(student2.school_name)  # دانشگاه شریف
```

## 3. متد `__new__` در مقابل `__init__`

```python
class Example:
    def __new__(cls):
        print("__new__ اجرا شد")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self):
        print("__init__ اجرا شد")

obj = Example()
# خروجی:
# __new__ اجرا شد
# __init__ اجرا شد
```

- `__new__`: شی را می‌سازد (constructor)
- `__init__`: شی را مقداردهی می‌کند (initializer)

## 4. الگوی Singleton

### مشکل: چندین نمونه از یک کلاس

```python
class DatabaseConnection:
    def __init__(self):
        print("اتصال جدید به دیتابیس برقرار شد")

# هر بار اتصال جدید!
db1 = DatabaseConnection()  # اتصال جدید به دیتابیس برقرار شد
db2 = DatabaseConnection()  # اتصال جدید به دیتابیس برقرار شد
print(db1 is db2)  # False - دو شی متفاوت هستند
```

### راه‌حل: Singleton Pattern

```python
class Database:
    _instance = None  # متغیر کلاس برای نگهداری تک نمونه
    
    def __new__(cls):
        if cls._instance is None:
            print("اولین بار دیتابیس ساخته می‌شود")
            cls._instance = super().__new__(cls)
        else:
            print("دیتابیس قبلاً ساخته شده، همان نمونه برگردانده می‌شود")
        return cls._instance
    
    def __init__(self):
        print("مقداردهی شی")

# تست
db1 = Database()
db2 = Database()
print(f"db1 is db2: {db1 is db2}")  # True
```

## 5. Singleton با تنظیمات پیش‌فرض

```python
class Config:
    _instance = None
    _default_settings = {
        "debug": True,
        "database_url": "localhost:5432",
        "timeout": 30
    }
    
    def __new__(cls, settings=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(settings)
        return cls._instance
    
    def _initialize(self, settings):
        """این متد فقط یک بار اجرا می‌شود"""
        if settings:
            self.settings = settings
        else:
            self.settings = self._default_settings.copy()
        print(f"تنظیمات بارگذاری شد: {self.settings}")

# تست
config1 = Config()  # تنظیمات پیش‌فرض
config2 = Config({"debug": False})  # تنظیمات جدید نادیده گرفته می‌شود
print(config1.settings)
print(config2.settings)
print(config1 is config2)  # True
```

## 6. مثال عملی: مدیریت لاگ

```python
class Logger:
    _instance = None
    _default_config = {
        "level": "INFO",
        "format": "%(asctime)s - %(message)s",
        "file": "app.log"
    }
    
    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(config)
        return cls._instance
    
    def _initialize(self, config):
        self.config = config if config else self._default_config
        self.logs = []
        print(f"Logger آماده شد با تنظیمات: {self.config}")
    
    def log(self, message):
        log_entry = f"[{self.config['level']}] {message}"
        self.logs.append(log_entry)
        print(log_entry)

# استفاده
logger1 = Logger()
logger1.log("سیستم راه‌اندازی شد")

logger2 = Logger()  # همان نمونه قبلی
logger2.log("کاربر وارد شد")

print(f"تعداد لاگ‌ها: {len(logger1.logs)}")  # 2
print(logger1 is logger2)  # True
```

## 7. مزایا و معایب Singleton

### مزایا:
- کنترل بر تعداد نمونه‌ها
- صرفه‌جویی در منابع
- دسترسی سراسری به یک نمونه

### معایب:
- سخت‌تر برای تست
- نقض اصل Single Responsibility
- مشکل در برنامه‌های چندنخی

## 8. نکات مهم

### نکته 1: تفاوت `_variable` و `__variable`

```python
class Test:
    _protected = "محافظت شده"      # قرارداد که از خارج دسترسی نداشته باش
    __private = "خصوصی"           # واقعاً خصوصی (name mangling)

obj = Test()
print(obj._protected)    # کار می‌کند ولی بهتر نیست
# print(obj.__private)   # خطا! AttributeError
print(obj._Test__private) # کار می‌کند ولی بد است
```

### نکته 2: مشکل Singleton در threading

```python
import threading

class UnsafeSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# ممکن است در حالت چندنخی مشکل داشته باشد
```

### نکته 3: Singleton امن برای threading

```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

## 9. تمرین‌ها

1. یک کلاس `Cache` بنویسید که از Singleton استفاده کند
2. یک کلاس `GameSettings` بسازید که تنظیمات بازی را نگهداری کند
3. کلاس `Database` را طوری بنویسید که بتواند تنظیمات را بعداً تغییر دهد

## خلاصه

- **`_instance = None`**: متغیر کلاس برای نگهداری تک نمونه
- **`_default_config`**: تنظیمات پیش‌فرض
- **`__new__`**: متد سازنده که قبل از `__init__` اجرا می‌شود
- **`_initialize`**: متد مقداردهی که فقط یک بار اجرا می‌شود
- **Singleton**: الگوی طراحی که فقط یک نمونه از کلاس اجازه می‌دهد

این الگو برای کلاس‌هایی مثل دیتابیس، لاگر، تنظیمات، و کش بسیار مفید است.