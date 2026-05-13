import asyncio
from app.agents import decomposer, rag, critic, synthesis, compression
from app.models.context import AgentContext
from app.utils.logging import log_event

class Orchestrator:
    def __init__(self):
        self.context = None

    async def execute(self, job_id: str, query: str):
        self.context = AgentContext(job_id=job_id, original_query=query, token_budget=8000)
        await log_event(job_id, "orchestrator_started", {"query": query})
        
        # 1. Dynamic LLM-driven plan
        plan = await decomposer.generate_plan(query)
        if not plan or "subtasks" not in plan:
            plan = {"subtasks": {"T1": {"type": "rag", "description": "Fulfill query", "depends_on": []}}}
            
        await log_event(job_id, "plan_generated", {"plan": plan})
        
        # 2. Resolve dependencies
        order = await decomposer.resolve_dependencies(plan.get("subtasks", {}))
        
        # 3. Execute in DAG order
        for tid in order:
            task_info = plan["subtasks"][tid]
            task_type = task_info.get("type", "rag")
            task_desc = task_info.get("description", "")
            
            if self.context.check_remaining_budget() < 1500:
                await log_event(job_id, "compression_triggered", {"budget_remaining": self.context.check_remaining_budget()})
                self.context = await compression.compress(self.context)
            
            self.context.execution_trace.append({"task": tid, "status": "started", "type": task_type})
            await asyncio.sleep(0.01) # Yield for streaming
            
            # Route to agent
            if task_type == "rag":
                await rag.execute(task_desc, self.context, tid)
                # Automatically run critique on rag outputs as required
                await critic.execute(f"Review findings from task {tid}", self.context, f"{tid}_critic")
            elif task_type == "critic":
                await critic.execute(task_desc, self.context, tid)
                
            self.context.execution_trace.append({"task": tid, "status": "completed"})

        # 4. Final synthesis
        await synthesis.execute(self.context)
        await log_event(job_id, "orchestrator_completed", {"final_tokens": self.context.tokens_used})
        return self.context