from app.utils.llm import generate_json
from app.db.database import AsyncSessionLocal
from app.db.models import PromptRewrite

async def analyze_failures(failed_cases: list):
    prompt = f"""
    Analyze the following failed test cases to identify the worst-performing agent/dimension.
    Propose a rewritten prompt for that agent.
    
    Failed Cases:
    {failed_cases}
    
    Return JSON:
    {{
        "agent_id": "rag|critic|synthesis|decomposer",
        "dimension": "e.g., contradiction_resolution",
        "proposed_rewrite": "New improved system prompt...",
        "justification": "Why this is better"
    }}
    """
    
    result = await generate_json(prompt, system_prompt="You are a meta-optimization agent.")
    
    if "agent_id" in result:
        async with AsyncSessionLocal() as session:
            rewrite = PromptRewrite(
                agent_id=result["agent_id"],
                dimension=result.get("dimension", ""),
                content="<old prompt>",
                proposed_rewrite=result["proposed_rewrite"],
                justification=result.get("justification", "")
            )
            session.add(rewrite)
            await session.commit()
            return rewrite.id
    return None