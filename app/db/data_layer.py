import asyncpg
import asyncio
from typing import Dict, List, Any, Union, Optional
from .cls import Database
import logging

db = Database(
    {
        "user": "postgres",
        "password": "1234",
        "database": "social_chat_bot",
        "host": "localhost",
    }
)

#  Get Next Question from database
async def get_next_question(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve the number of the last answered question
    and the username of the user,
    and fetch the next question that needs to be answered
    based on the order of questions.
    """

    # query = """
    #     SELECT q.id, q.text
    #     FROM dialog.questions q
    #     WHERE q.user_id = $1
    #     AND NOT EXISTS (
    #         SELECT 1 FROM dialog.answers a
    #         WHERE a.user_id = $1 AND a.question_id = q.id
    #     )
    #     ORDER BY q.created_at ASC
    #     LIMIT 1
    # """
    # query = """
    #     SELECT q.id, q.text
    #     FROM dialog.questions q
    #     WHERE q.user_id = $1
    #     AND NOT EXISTS (
    #         SELECT 1 FROM dialog.answers a
    #         WHERE a.user_id = $1 AND a.question_id = q.id
    #     )
    #     ORDER BY q.created_at ASC
    #     LIMIT 1
    # """
    query = """
   SELECT text FROM dialog.questions
    """
    result = await db.execute_select(query, {})
    # result = await db.execute_select(query, {"user_id": user_id})
    # print(result)
    # return result
    return result if result else None


async def getQuestions(user):
    await db.connect()
    questions = await get_next_question(user_id=100)  # get question list
    output_list = [item["text"] for item in questions]  # convert dic to list

    # print(output_list)

    # لیست سؤالات
    # questions = [
    #     "نام و نام خانوادگی",
    #     "نام شرکت مطبوع",
    #     "پست سازمانی",
    #     "شماره همراه",
    #     "عنوان پیشنهاد سازمانی ",
    #     "حوزه مرتبط (بهره برداری - مهندی - مشترکین - مالی - منابع انسانی - فرآیندها - مدیریت) ",
    #     "کلمات کلیدی",
    #     "شرح مساله",
    #     "شرح نوآوری",
    #     "توضیحات تکمیلی ",
    # ]

    # get last answered question number to found next question to ask

    return output_list

  
async def run_query(query,parameters):
    
    # await db.connect()
    
    # new_user_id = await db.execute_insert(
    #     query="INSERT INTO users (name, email, age) VALUES ($1, $2, $3)",
    #     params={'name': 'علی', 'email': 'ali@example.com', 'age': 25}
    # )
    # print(f"شناسه کاربر جدید: {new_user_id}")

    
    # result = await db.execute_update(
    #     query="""
    #     UPDATE products 
    #     SET price = price * $1 
    #     WHERE category = $2 
    #     RETURNING id, name, price
    #     """,
    #     params={'factor': 1.1, 'category': 'electronics'},
    #     returning=True
    # )
    
  
    return 
    