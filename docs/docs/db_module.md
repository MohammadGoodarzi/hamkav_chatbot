
## آموزش استفاده از select داده از دیتابیس

```python
 db = Database({
        'user': 'postgres',
        'password': '1234',
        'database': 'social_chat_bot',
        'host': 'localhost'
    })
    
    await db.connect()
    
    try:
        # results = await db.execute_select(
        #     "SELECT * FROM users WHERE age > $1",
        #     {'age': 20}
        # )
        results = await db.execute_select(
            "SELECT * FROM dialog.question2",{}
        )
        print(results)
    finally:
        await db.close()
```

## روش استفاده از تابع به روز رسانی دیتابیس
```python
async with Database(db_config) as db:
    # مثال ۱: آپدیت ساده با پارامترهای دیکشنری
    affected_rows = await db.execute_update(
        query="UPDATE users SET status = $1 WHERE age < $2",
        params={'status': 'inactive', 'age': 18}
    )
    print(f"تعداد کاربران غیرفعال شده: {affected_rows}")

    # مثال ۲: آپدیت با RETURNING
    updated_products = await db.execute_update(
        query="""
        UPDATE products 
        SET price = price * $1 
        WHERE category = $2 
        RETURNING id, name, price
        """,
        params={'factor': 1.1, 'category': 'electronics'},
        returning=True
    )
    for product in updated_products:
        print(f"محصول به‌روز شده: {product['name']} با قیمت جدید {product['price']}")
        ```