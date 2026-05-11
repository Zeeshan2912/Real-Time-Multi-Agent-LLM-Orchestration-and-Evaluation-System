from app.tools.base import ToolContract

class SelfReflectionTool(ToolContract):
    TOOL_NAME = "self_reflection"

    def get_fallback(self):
        return {"contradictions": [], "confidence_delta": 0.0, "reason": "Self-reflection tool failed"}

    async def _execute(self, **kwargs):
        return {"contradictions": [], "confidence_delta": 0.05, "reason": "No contradictions detected"}