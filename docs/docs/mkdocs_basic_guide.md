# MkDocs-Material راهنمای نصب و استفاده

## نصب

### پیش‌نیازها
- Python 3.7 یا بالاتر
- pip (مدیر بسته Python)

### نصب MkDocs-Material

```bash
# نصب MkDocs-Material
pip install mkdocs-material

# نصب پلاگین‌های اضافی (اختیاری)
pip install mkdocs-git-revision-date-localized-plugin
pip install mkdocs-minify-plugin
pip install mkdocs-redirects
```

## ایجاد پروژه جدید

### روش 1: پروژه جدید
```bash
# ایجاد پروژه جدید
mkdocs new my-documentation
cd my-documentation
```

### روش 2: در فولدر موجود
```bash
# در فولدر موجود
mkdocs new .
```

## ساختار پروژه

پس از ایجاد پروژه، ساختار زیر ایجاد می‌شود:

```
my-documentation/
├── mkdocs.yml          # فایل کانفیگ اصلی
├── docs/               # فولدر فایل‌های markdown
│   └── index.md        # صفحه اصلی
└── site/               # فایل‌های build شده (بعد از build)
```

## کانفیگ پایه (mkdocs.yml)

```yaml
site_name: مستندات من
site_description: توضیحات مختصر پروژه
site_author: نام نویسنده
site_url: https://example.com

# Theme Configuration
theme:
  name: material
  language: fa  # برای فارسی
  direction: rtl  # برای فارسی
  
  # Color Palette
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: تغییر به حالت تیره
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: تغییر به حالت روشن
  
  # Features
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.tracking
    - search.suggest
    - search.highlight
    - search.share
    - content.tabs.link
    - content.code.annotation
    - content.code.copy
    - content.tooltips
    - toc.integrate

  # Custom Icons
  icon:
    repo: fontawesome/brands/github
    edit: material/pencil
    view: material/eye

# Navigation
nav:
  - خانه: index.md
  - شروع کار:
    - نصب: getting-started/installation.md
    - کانفیگ: getting-started/configuration.md
  - راهنمای کاربری:
    - مقدمه: user-guide/introduction.md
    - ویژگی‌ها: user-guide/features.md
  - API:
    - نقاط پایانی: api/endpoints.md
    - احراز هویت: api/authentication.md
  - درباره ما: about.md

# Plugins
plugins:
  - search:
      lang: fa
  - git-revision-date-localized:
      type: date
      timezone: Asia/Tehran
  - minify:
      minify_html: true
  - redirects:
      redirect_maps:
        'old-page.md': 'new-page.md'

# Markdown Extensions
markdown_extensions:
  # Code Highlighting
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  
  # Content Enhancement
  - admonition
  - pymdownx.details
  - pymdownx.critic
  - pymdownx.caret
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.tilde
  
  # Lists and Tables
  - def_list
  - pymdownx.tasklist:
      custom_checkbox: true
  - tables
  
  # Links and References
  - attr_list
  - md_in_html
  - abbr
  - footnotes
  
  # Math
  - pymdownx.arithmatex:
      generic: true
  
  # Emojis
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg
  
  # Tabs
  - pymdownx.tabbed:
      alternate_style: true

# Extra CSS and JS
extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# Extra Configuration
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/username
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/username
    - icon: fontawesome/brands/linkedin
      link: https://linkedin.com/in/username
  
  analytics:
    provider: google
    property: G-XXXXXXXXXX
  
  generator: false  # حذف "Made with MkDocs"

# Copyright
copyright: Copyright &copy; 2024 - 2025 نام شما

# Repository
repo_url: https://github.com/username/repository
repo_name: username/repository
edit_uri: edit/main/docs/
```

## ایجاد محتوای اولیه

### فایل index.md

```markdown
# خوش آمدید به مستندات

این صفحه اصلی مستندات شما است.

## ویژگی‌ها

- طراحی زیبا و مدرن
- پشتیبانی کامل از فارسی
- جستجوی پیشرفته
- تم تیره و روشن

## شروع سریع

برای شروع، [راهنمای نصب](getting-started/installation.md) را مطالعه کنید.

!!! tip "نکته"
    این یک نکته مفید است!

!!! warning "هشدار"
    مراقب این مورد باشید!

!!! danger "خطر"
    این مورد خطرناک است!
```

## دستورات اساسی

### Development Server

```bash
# اجرای سرور توسعه
mkdocs serve

# اجرای روی پورت مشخص
mkdocs serve --dev-addr=localhost:8080

# اجرای با reload خودکار
mkdocs serve --livereload
```

### Build کردن

```bash
# Build برای production
mkdocs build

# Build با پاک کردن فایل‌های قبلی
mkdocs build --clean

# Build در مسیر مشخص
mkdocs build --site-dir /path/to/site
```

### Deploy

```bash
# Deploy به GitHub Pages
mkdocs gh-deploy

# Deploy با پیام commit مشخص
mkdocs gh-deploy --message "Update documentation"

# Deploy به branch مشخص
mkdocs gh-deploy --remote-branch gh-pages
```

## ایجاد فایل‌های CSS و JS سفارشی

### فایل CSS سفارشی

```bash
# ایجاد فولدر stylesheets
mkdir docs/stylesheets
```

```css
/* docs/stylesheets/extra.css */
:root {
  --md-primary-fg-color: #1976d2;
  --md-accent-fg-color: #ff4081;
}

/* استایل‌های فارسی */
.md-typeset h1,
.md-typeset h2,
.md-typeset h3 {
  font-family: 'Vazir', sans-serif;
}

/* استایل‌های سفارشی */
.custom-callout {
  background: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 1rem;
  margin: 1rem 0;
}
```

### فایل JavaScript سفارشی

```bash
# ایجاد فولدر javascripts
mkdir docs/javascripts
```

```javascript
// docs/javascripts/extra.js
document.addEventListener('DOMContentLoaded', function() {
  // کد سفارشی شما
  console.log('Documentation loaded');
});
```

## نکات مهم

### 1. پشتیبانی از فارسی

```yaml
# در mkdocs.yml
theme:
  name: material
  language: fa
  direction: rtl
  
plugins:
  - search:
      lang: fa
```

### 2. کش کردن

```bash
# پاک کردن کش
rm -rf site/
mkdocs build --clean
```

### 3. تست کردن

```bash
# تست لینک‌های شکسته
mkdocs build --strict
```

### 4. مدیریت تصاویر

```
docs/
├── images/
│   ├── logo.png
│   └── screenshots/
│       └── app.png
└── index.md
```

```markdown
![Logo](images/logo.png)
![Screenshot](images/screenshots/app.png)
```

## عیب‌یابی رایج

### مشکل 1: خطای Import

```bash
# نصب مجدد
pip uninstall mkdocs-material
pip install mkdocs-material
```

### مشکل 2: مشکل Encoding

```python
# در فایل‌های Python
# -*- coding: utf-8 -*-
```

### مشکل 3: مشکل Navigation

```yaml
# مطمئن شوید فایل‌ها وجود دارند
nav:
  - Home: index.md  # باید در docs/ باشد
  - About: about.md # باید در docs/ باشد
```

## منابع مفید

- [مستندات رسمی MkDocs](https://www.mkdocs.org/)
- [مستندات MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
- [Material Icons](https://fonts.google.com/icons?selected=Material+Icons)

## نتیجه‌گیری

MkDocs-Material ابزاری قدرتمند برای ایجاد مستندات زیبا و کاربردی است. با پیروی از این راهنما، می‌توانید به راحتی مستندات حرفه‌ای ایجاد کنید.