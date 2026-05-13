from app.tools.base import ToolContract
import asyncio

class WebSearchTool(ToolContract):
    TOOL_NAME = "web_search"

    def get_fallback(self):
        return [{"title": "Fallback Search", "snippet": "Search service unavailable.", "url": "", "score": 0.0}]

    def validate_input(self, **kwargs) -> bool:
        return "query" in kwargs and isinstance(kwargs["query"], str)

    async def _execute(self, **kwargs):
        query = kwargs.get("query", "")
        if "timeout" in query.lower():
            await asyncio.sleep(15) # Force timeout
        if "empty" in query.lower():
            return []
            
        return [
            {"title": f"Result 1 for {query}", "snippet": f"This is a detailed snippet about {query}.", "url": "https://example.com/1", "score": 0.95},
            {"title": f"Result 2 for {query}", "snippet": "Another relevant snippet.", "url": "https://example.com/2", "score": 0.88}
        ]