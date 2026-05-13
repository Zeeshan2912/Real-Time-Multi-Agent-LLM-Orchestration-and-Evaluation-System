import asyncio
import sys
from app.tools.base import ToolContract

class CodeSandboxTool(ToolContract):
    TOOL_NAME = "code_sandbox"

    def get_fallback(self):
        return {"stdout": "", "stderr": "Code execution failed or timed out.", "exit_code": -1}

    def validate_input(self, **kwargs) -> bool:
        return "code" in kwargs and isinstance(kwargs["code"], str)

    async def _execute(self, **kwargs):
        code = kwargs.get("code")
        process = await asyncio.create_subprocess_exec(
            sys.executable, "-c", code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": process.returncode
        }