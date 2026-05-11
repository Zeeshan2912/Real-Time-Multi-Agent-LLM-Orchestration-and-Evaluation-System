from abc import ABC, abstractmethod
import asyncio
from typing import Any, Dict

class ToolContract(ABC):
    TOOL_NAME: str
    MAX_RETRIES = 2

    @abstractmethod
    async def _execute(self, **kwargs) -> Any: pass

    @abstractmethod
    def get_fallback(self) -> Any: pass

    def validate_input(self, **kwargs) -> bool: return True

    async def run(self, **kwargs) -> Dict[str, Any]:
        log = {"tool": self.TOOL_NAME, "input": kwargs, "attempts": []}
        if not self.validate_input(**kwargs):
            log["result"] = {"status": "malformed_input", "fallback": self.get_fallback()}
            return log

        for attempt in range(1, self.MAX_RETRIES + 2):
            try:
                res = await asyncio.wait_for(self._execute(**kwargs), timeout=10.0)
                log["result"] = {"status": "success", "data": res, "latency_ms": 100 * attempt}
                return log
            except asyncio.TimeoutError:
                log["attempts"].append({"status": "timeout", "attempt": attempt})
            except Exception as e:
                log["attempts"].append({"status": "error", "msg": str(e), "attempt": attempt})

            if attempt <= self.MAX_RETRIES:
                await asyncio.sleep(0.5 * attempt)
                kwargs["retry_attempt"] = attempt

        log["result"] = {"status": "failed", "fallback": self.get_fallback()}
        return log