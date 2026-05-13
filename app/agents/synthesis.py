from app.utils.llm import generate_text

async def execute(context):
    prompt = f"""
    Merge the following outputs from all sub-agents. 
    Resolve any contradictions flagged by the critique agent.
    Produce a final answer with a provenance map linking each sentence to its source agent and source chunk.
    
    Original Query: {context.original_query}
    
    Current State (Outputs):
    {context.current_state}
    
    Critique Flags (Resolve these):
    {context.span_flags}
    """
    
    final_answer = await generate_text(prompt, system_prompt="You are a final synthesis agent. Resolve all contradictions explicitly.")
    context.add_text_to_state(f"Synthesis Agent: {final_answer}")
    return final_answer