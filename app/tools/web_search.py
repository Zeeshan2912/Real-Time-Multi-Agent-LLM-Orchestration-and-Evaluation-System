from app.tools.base import ToolContract

class WebSearchTool(ToolContract):
    TOOL_NAME = "web_search"

    def get_fallback(self):
        return [{"title": "Fallback", "snippet": "Search service unavailable", "url": None, "score": 0.0}]

    async def _execute(self, **kwargs):
        return [
            {"title": f"Result for {kwargs.get('query')}", "snippet": "Mock structured data", "url": "https://example.com", "score": 0.85}
        ]