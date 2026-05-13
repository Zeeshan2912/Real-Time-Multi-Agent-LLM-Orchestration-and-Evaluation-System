from app.utils.llm import generate_text

async def compress(context):
    prompt = f"""
    Summarize the following conversational context to save tokens.
    Keep all structured data (tool outputs, scores, citations) lossless. 
    Compress only the conversational filler.
    
    Context:
    {context.current_state}
    """
    
    compressed_state = await generate_text(prompt, system_prompt="You are a lossless compression agent.")
    
    # Replace the state
    context.current_state = compressed_state
    
    # Recalculate tokens completely (lossy but accurate for remaining budget)
    context.tokens_used = context.count_tokens(compressed_state)
    return context