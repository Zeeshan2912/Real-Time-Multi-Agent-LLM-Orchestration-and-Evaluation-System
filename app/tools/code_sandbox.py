from app.tools.base import ToolContract

class CodeSandboxTool(ToolContract):
    TOOL_NAME = "code_sandbox"

    def validate_input(self, **kwargs):
        code = kwargs.get("code", "")
        return bool(code) and "exec(" not in code and "__import__" not in code

    def get_fallback(self):
        return {"stdout": "", "stderr": "Sandbox execution unavailable", "exit_code": 1}

    async def _execute(self, **kwargs):
        return {"stdout": "Mock output (42)\n", "stderr": "", "exit_code": 0}