from app.tools.base import ToolContract
from app.utils.llm import generate_json

class SelfReflectionTool(ToolContract):
    TOOL_NAME = "self_reflection"

    def get_fallback(self):
        return {"contradictions_found": []}

    def validate_input(self, **kwargs) -> bool:
        return "context_state" in kwargs

    async def _execute(self, **kwargs):
        context_state = kwargs.get("context_state", "")
        prompt = f"Analyze the following agent outputs for internal contradictions.\nOutputs:\n{context_state}\n\nReturn a JSON object with a list 'contradictions_found'."
        result = await generate_json(prompt, system_prompt="You are a logic analyzer.")
        return result