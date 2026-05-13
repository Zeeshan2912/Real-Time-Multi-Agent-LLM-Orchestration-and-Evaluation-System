from abc import ABC, abstractmethod
import asyncio
from typing import Any, Dict

class ToolContract(ABC):
    TOOL_NAME: str

    @abstractmethod
    async def _execute(self, **kwargs) -> Any: pass

    @abstractmethod
    def get_fallback(self) -> Any: pass

    def validate_input(self, **kwargs) -> bool: return True

    async def run(self, **kwargs) -> Dict[str, Any]:
        log = {"tool": self.TOOL_NAME, "input": kwargs}
        if not self.validate_input(**kwargs):
            log["result"] = {"status": "malformed_input", "fallback": self.get_fallback()}
            return log

        try:
            res = await asyncio.wait_for(self._execute(**kwargs), timeout=10.0)
            log["result"] = {"status": "success", "data": res, "latency_ms": 100}
            return log
        except asyncio.TimeoutError:
            log["result"] = {"status": "timeout", "fallback": self.get_fallback()}
        except Exception as e:
            log["result"] = {"status": "error", "msg": str(e), "fallback": self.get_fallback()}

        return log