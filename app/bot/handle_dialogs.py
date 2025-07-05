"""
In this file we handle questions and answers and thair sequences (order of asking)

"""

from typing import Dict, List, Any, Union, Optional
from db.cls import Database
import logging

db = Database({
        'user': 'postgres',
        'password': '1234',
        'database': 'social_chat_bot',
        'host': 'localhost'
    })
    
await db.connect()


#  Get Next Question from database
async def get_next_question(user_id: int) -> Optional[Dict[str, Any]]:
    query = """
        SELECT q.id, q.text
        FROM dialog.questions q
        WHERE q.user_id = $1
        AND NOT EXISTS (
            SELECT 1 FROM dialog.answers a
            WHERE a.user_id = $1 AND a.question_id = q.id
        )
        ORDER BY q.created_at ASC
        LIMIT 1
    """
    result = await db.execute_select(query, {"user_id": user_id})
    return result[0] if result else None

# Store User Response to database