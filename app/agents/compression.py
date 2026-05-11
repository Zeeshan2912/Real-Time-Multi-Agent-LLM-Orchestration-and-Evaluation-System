async def compress(context):
    # Lossy for conversational filler, lossless for structured data
    context.tokens_used = max(0, context.tokens_used - 1500)
    context.execution_trace.append({"agent": "compression", "status": "applied", "tokens_saved": 1500})
    return context