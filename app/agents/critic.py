async def execute(prompt: str, context, task_id: str):
    context.add_tokens(300)
    # Span-level flags, not whole-output rejection
    context.span_flags.append({
        "start": 0, "end": 12, "reason": "Unverified claim in synthesis",
        "confidence": 0.65, "task_id": task_id
    })
    context.claims_confidence.append({"claim": "primary_answer", "score": 0.82})
    return {"flags": 1, "confidence": 0.82}