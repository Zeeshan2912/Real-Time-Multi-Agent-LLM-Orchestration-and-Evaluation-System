from app.utils.llm import generate_json

async def execute(instruction: str, context, task_id: str):
    state_so_far = context.current_state
    
    prompt = f"""
    Review the following agent outputs. 
    Assign a structured confidence score (0.0 to 1.0) per claim, and flag specific spans of text you disagree with.
    
    Outputs:
    {state_so_far}
    
    Return JSON with two keys:
    "claims_confidence": list of {{"claim": "...", "score": 0.8}}
    "span_flags": list of {{"span": "...", "reason": "..."}}
    """
    
    schema = {
        "claims_confidence": [{"claim": "string", "score": 0.0}],
        "span_flags": [{"span": "string", "reason": "string"}]
    }
    
    result = await generate_json(prompt, system_prompt="You are a strict critique agent.", schema=schema)
    
    if "claims_confidence" in result:
        context.claims_confidence.extend(result["claims_confidence"])
    if "span_flags" in result:
        for sf in result["span_flags"]:
            context.span_flags.append({
                "type": "critique_disagreement",
                "span": sf.get("span"),
                "detail": sf.get("reason"),
                "agent": f"critic_{task_id}"
            })
            
    return result