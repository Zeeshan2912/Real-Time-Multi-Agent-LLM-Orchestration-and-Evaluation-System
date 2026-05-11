async def propose_rewrite(failed_case: dict) -> dict:
    return {
        "rewrite_id": f"meta_{failed_case.get('id', 'unknown')}",
        "proposed_prompt": f"[OPTIMIZED] {failed_case.get('input', '')}",
        "expected_delta": "+8% accuracy",
        "requires_approval": True,
        "dimension_targeted": "answer_correctness"
    }