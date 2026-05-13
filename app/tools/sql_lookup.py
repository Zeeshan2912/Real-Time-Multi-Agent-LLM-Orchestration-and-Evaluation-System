from app.tools.base import ToolContract
from app.utils.llm import generate_text
from sqlalchemy import text
from app.db.database import AsyncSessionLocal

class SQLLookupTool(ToolContract):
    TOOL_NAME = "sql_lookup"

    def get_fallback(self):
        return {"error": "SQL Lookup failed.", "data": []}

    def validate_input(self, **kwargs) -> bool:
        return "nl_query" in kwargs and isinstance(kwargs["nl_query"], str)

    async def _execute(self, **kwargs):
        nl_query = kwargs.get("nl_query")
        
        prompt = f"Convert this natural language query to a SQL SELECT query for PostgreSQL. Only output the SQL query, nothing else. Query: {nl_query}"
        sql_query = await generate_text(prompt, system_prompt="You are a SQL expert.")
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        if not sql_query.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")
            
        async with AsyncSessionLocal() as session:
            result = await session.execute(text(sql_query))
            data = [dict(row._mapping) for row in result]
            
        return {"sql_executed": sql_query, "data": data}