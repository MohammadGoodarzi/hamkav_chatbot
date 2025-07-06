# استانداردهای کدنویسی تیم (Team Coding Standards)

## مقدمه (Overview)
این سند استانداردهای کدنویسی (Coding Standards) را برای تضمین یکنواختی (Consistency)، قابلیت نگهداری (Maintainability) و همکاری (Collaboration) در تیم توسعه تعیین می‌کند.

## اصول کلی (General Principles)

### کیفیت کد (Code Quality)
- **خوانایی اول (Readability First)**: کدی بنویسید که داستان تعریف کند
- **یکنواختی (Consistency)**: از الگوهای مشخص شده در کل کدبیس (Codebase) پیروی کنید
- **سادگی (Simplicity)**: راه‌حل‌های ساده و واضح را بر راه‌حل‌های باهوش ترجیح دهید
- **مستندسازی (Documentation)**: کد باید با نام‌های معنادار خود-مستند باشد

### همکاری (Collaboration)
- **همه چیز را بررسی کنید (Review Everything)**: همه تغییرات کد نیاز به بررسی همتا (Peer Review) دارند
- **قصد را انتقال دهید (Communicate Intent)**: از پیام‌های کامیت (Commit Messages) و توضیحات PR واضح استفاده کنید
- **دانش را به اشتراک بگذارید (Share Knowledge)**: تصمیمات و انتخاب‌های معماری (Architectural Choices) را مستند کنید

## فرمت‌بندی و استایل (Formatting & Style)

### تورفتگی (Indentation)
- از 2 فاصله برای تورفتگی استفاده کنید (بدون Tab)
- تورفتگی یکنواخت در همه فایل‌ها

### طول خط (Line Length)
- حداکثر 100 کاراکتر در هر خط
- خطوط طولانی را در نقاط منطقی بشکنید

### قراردادهای نام‌گذاری (Naming Conventions)
- **متغیرها و توابع (Variables & Functions)**: camelCase (`getUserData`, `isActive`)
- **ثابت‌ها (Constants)**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **کلاس‌ها (Classes)**: PascalCase (`UserService`, `PaymentProcessor`)
- **فایل‌ها (Files)**: kebab-case (`user-service.js`, `payment-utils.js`)

### کامنت‌ها (Comments)
- از کامنت‌ها برای توضیح *چرا* استفاده کنید، نه *چی*
- کامنت‌ها را با تغییرات کد به‌روز نگه دارید
- از JSDoc/docstrings برای مستندسازی توابع استفاده کنید

## سازماندهی کد (Code Organization)

### ساختار فایل (File Structure)
```
src/
├── components/          # کامپوننت‌های قابل استفاده مجدد UI
├── services/           # منطق کسب‌وکار و فراخوانی API
├── utils/              # توابع کمکی Helper Functions
├── constants/          # ثابت‌های برنامه Application Constants
├── types/              # تعاریف نوع Type Definitions
└── tests/              # فایل‌های تست Test Files
```

### سازماندهی Import
1. کتابخانه‌های خارجی (External Libraries)
2. ماژول‌های داخلی (Internal Modules) - مطلق (Absolute Imports)
3. Import های نسبی (Relative Imports)
4. گروه‌ها را با خط خالی جدا کنید

## بهترین روش‌ها (Best Practices)

### توابع (Functions)
- توابع را کوچک و متمرکز نگه دارید (< 20 خط در صورت امکان)
- از نام‌های توصیفی برای پارامترها (Parameters) استفاده کنید
- از نستینگ عمیق (Deep Nesting) اجتناب کنید (حداکثر 3 سطح)
- برای کاهش پیچیدگی (Complexity) زود برگردید

### مدیریت خطا (Error Handling)
- همیشه خطاها را صریحاً مدیریت کنید
- از بلوک‌های try-catch به درستی استفاده کنید
- پیام‌های خطای معنادار ارائه دهید
- خطاها را با محتوای کافی لاگ کنید

### تست (Testing)
- برای همه ویژگی‌های جدید تست بنویسید
- هدف 80%+ پوشش کد (Code Coverage) باشد
- از نام‌های توصیفی برای تست‌ها استفاده کنید
- از الگوی AAA پیروی کنید (Arrange, Act, Assert)

### عملکرد (Performance)
- از بهینه‌سازی زودهنگام (Premature Optimization) اجتناب کنید
- قبل از بهینه‌سازی پروفایل (Profile) کنید
- از ساختار داده‌های مناسب (Data Structures) استفاده کنید
- در حلقه‌ها استفاده از حافظه (Memory Usage) را در نظر بگیرید

## کنترل نسخه (Version Control)

### پیام‌های کامیت (Commit Messages)
فرمت: `type: توضیح مختصر`

انواع (Types):
- `feat`: ویژگی جدید (New Feature)
- `fix`: رفع باگ (Bug Fix)
- `docs`: تغییرات مستندات (Documentation Changes)
- `style`: تغییرات استایل کد (Code Style Changes)
- `refactor`: بازسازی کد (Code Refactoring)
- `test`: اضافه/تغییر تست‌ها (Test Additions/Changes)
- `chore`: وظایف نگهداری (Maintenance Tasks)

مثال: `feat: add user authentication middleware`

### نام‌گذاری شاخه (Branch Naming)
- `feature/description` برای ویژگی‌های جدید
- `bugfix/description` برای رفع باگ‌ها
- `hotfix/description` برای رفع‌های فوری

### درخواست‌های Pull (Pull Requests)
- از عناوین و توضیحات توصیفی استفاده کنید
- مسائل مرتبط را لینک کنید
- PR ها را متمرکز و کوچک نگه دارید
- در صورت نیاز مستندات را به‌روز کنید

## راهنمایی‌های امنیتی (Security Guidelines)

### مدیریت داده (Data Handling)
- هرگز داده‌های حساس (رمز عبور، کلیدهای API) را کامیت نکنید
- از متغیرهای محیطی (Environment Variables) برای کانفیگ استفاده کنید
- همه ورودی‌ها را اعتبارسنجی (Validate) و پاکسازی (Sanitize) کنید
- از کوئری‌های پارامتری (Parameterized Queries) برای عملیات دیتابیس استفاده کنید

### احراز هویت (Authentication)
- مدیریت جلسه مناسب (Session Management) پیاده‌سازی کنید
- از HTTPS برای همه ارتباطات استفاده کنید
- رمزهای عبور را به صورت امن ذخیره کنید (هش + نمک)
- کنترل دسترسی مناسب (Access Controls) پیاده‌سازی کنید

## مستندسازی (Documentation)

### مستندسازی کد (Code Documentation)
- الگوریتم‌های پیچیده و منطق کسب‌وکار را مستند کنید
- فایل‌های README برای هر کامپوننت اصلی نگهداری کنید
- مستندات API را به‌روز نگه دارید
- رویه‌های استقرار (Deployment) و راه‌اندازی (Setup) را مستند کنید

### تصمیمات معماری (Architecture Decisions)
- تصمیمات معماری مهم را ثبت کنید
- مبادلات (Trade-offs) و جایگزین‌های در نظر گرفته شده را مستند کنید
- هنگام تغییر معماری، مستندات را به‌روز کنید

## فرآیند بررسی (Review Process)

### چک‌لیست بررسی کد (Code Review Checklist)
- [ ] کد از راهنمایی‌های استایل پیروی می‌کند
- [ ] توابع نام‌گذاری مناسب و متمرکز دارند
- [ ] مدیریت خطا مناسب است
- [ ] تست‌ها شامل و موفق هستند
- [ ] مستندات به‌روز شده است
- [ ] آسیب‌پذیری امنیتی وجود ندارد
- [ ] ملاحظات عملکرد بررسی شده است

### راهنمایی‌های بررسی (Review Guidelines)
- سازنده و محترمانه باشید
- روی کد تمرکز کنید، نه شخص
- دلیل پیشنهادات را توضیح دهید
- هنگام رعایت استانداردها تأیید کنید

## ابزارها و اتوماسیون (Tools & Automation)

### لینتینگ (Linting)
- از ESLint/Prettier برای JavaScript/TypeScript استفاده کنید
- هوک‌های پیش-کامیت (Pre-commit Hooks) را کانفیگ کنید
- با پایپ‌لاین CI/CD ادغام کنید

### تست (Testing)
- اجرای تست خودکار روی همه PR ها
- گزارش پوشش (Coverage Reporting)
- بنچمارک عملکرد (Performance Benchmarking) برای مسیرهای حیاتی

### استقرار (Deployment)
- استقرار خودکار از شاخه اصلی (Main Branch)
- محیط استیجینگ (Staging Environment) برای تست
- رویه‌های بازگشت (Rollback Procedures) مستند شده

## اجرا (Enforcement)

### پذیرش تدریجی (Gradual Adoption)
- استانداردها را فوراً به کد جدید اعمال کنید
- کد موجود را به صورت فرصت‌طلبانه بازسازی کنید
- بررسی منظم تیمی از استانداردها

### بهبود مستمر (Continuous Improvement)
- جلسات بررسی ماهانه استانداردها
- بازخورد از اعضای تیم جمع‌آوری کنید
- استانداردها را بر اساس نیازهای پروژه به‌روز کنید
- با بهترین روش‌های صنعت (Industry Best Practices) همگام باشید

---

*این سند استانداردی زنده است که با نیازهای تیم و پروژه ما تکامل می‌یابد. همه اعضای تیم تشویق می‌شوند تا بهبودها و پیشنهادات ارائه دهند.*