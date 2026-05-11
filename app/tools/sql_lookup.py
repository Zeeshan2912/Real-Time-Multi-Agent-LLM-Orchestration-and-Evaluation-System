from app.tools.base import ToolContract

class SQLLookupTool(ToolContract):
    TOOL_NAME = "sql_lookup"

    def validate_input(self, **kwargs):
        q = kwargs.get("query", "").strip().upper()
        return q.startswith("SELECT") and not any(d in q for d in ["DROP", "DELETE", "UPDATE", "INSERT"])

    def get_fallback(self):
        return [{"error": "Database service unavailable"}]

    async def _execute(self, **kwargs):
        return [{"id": 1, "data": "mock_row", "matched": True}]