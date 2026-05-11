import asyncio
from app.agents import decomposer, rag, critic, synthesis, compression
from app.models.context import AgentContext

class Orchestrator:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.context = None

    async def execute(self, job_id: str, query: str):
        self.context = AgentContext(job_id=job_id, original_query=query, token_budget=8000)
        
        # 1. Dynamic LLM-driven plan (no hardcoded chains)
        plan = await self.llm.generate_json(f"Plan execution DAG for: {query}") if self.llm else {
            "subtasks": {"A": {"type": "rag", "depends_on": []}, "B": {"type": "critic", "depends_on": ["A"]}}
        }
        
        # 2. Resolve dependencies
        order = await decomposer.resolve_dependencies(plan.get("subtasks", {}))
        
        # 3. Execute in DAG order
        for tid in order:
            if self.context.check_remaining_budget() < 1500:
                self.context = await compression.compress(self.context)
            
            self.context.execution_trace.append({"task": tid, "status": "started"})
            await asyncio.sleep(0.02) # Yield for streaming
            
            # Route to agent
            await rag.execute(f"Task {tid}", self.context, tid)
            await critic.execute(f"Task {tid}", self.context, tid)
            self.context.execution_trace.append({"task": tid, "status": "completed"})

        # 4. Final synthesis
        await synthesis.execute([], self.context)
        return self.context