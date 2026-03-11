import aiosqlite3
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async def create_async_checkpointer():
    """Create and return an async SQLite checkpointer for conversation persistence"""
    conn = await aiosqlite3.connect("chatbot.db")
    checkpointer = AsyncSqliteSaver(conn=conn)
    return checkpointer