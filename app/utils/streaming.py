import json

def format_event(agent: str, status: str, token: str="", tool: str="", budget: int=0):
    return json.dumps({
        "agent_id": agent,
        "status": status,
        "token": token,
        "tool_in_flight": tool,
        "budget_remaining": budget
    }) + "\n"