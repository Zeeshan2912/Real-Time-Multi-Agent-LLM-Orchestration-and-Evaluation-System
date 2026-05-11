from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class AgentContext(BaseModel):
    job_id: str
    original_query: str
    current_state: str = ""
    token_budget: int = Field(default=8000, gt=0)
    tokens_used: int = 0
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    claims_confidence: List[Dict[str, float]] = Field(default_factory=list)
    tool_calls_log: List[Dict[str, Any]] = Field(default_factory=list)
    span_flags: List[Dict[str, Any]] = Field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def check_remaining_budget(self) -> int:
        return max(0, self.token_budget - self.tokens_used)

    def add_tokens(self, count: int):
        self.tokens_used += count
        if self.tokens_used > self.token_budget:
            self.span_flags.append({
                "type": "policy_violation",
                "detail": f"Overflowed by {self.tokens_used - self.token_budget} tokens",
                "agent": "context_manager"
            })