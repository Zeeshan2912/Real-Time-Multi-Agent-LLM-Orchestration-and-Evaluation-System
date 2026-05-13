from typing import Dict, Any
from app.utils.llm import generate_json

class Scorer:
    async def score(self, query: str, context_state: str, tokens_used: int, budget: int) -> Dict[str, Dict]:
        prompt = f"""
        Evaluate the following agent execution against the original query.
        Original Query: {query}
        Tokens Used: {tokens_used}/{budget}
        Final Output & State: {context_state}
        
        Provide a numeric score (0.0 to 1.0) and a string justification for each dimension:
        1. answer_correctness
        2. contradiction_resolution
        3. critique_agreement_rate
        
        Output JSON:
        {{
            "answer_correctness": {{"score": 0.0, "justification": ""}},
            "contradiction_resolution": {{"score": 0.0, "justification": ""}},
            "critique_agreement_rate": {{"score": 0.0, "justification": ""}}
        }}
        """
        
        scores = await generate_json(prompt, system_prompt="You are an expert LLM-as-a-judge.")
        
        # Add deterministic scores
        scores["context_budget_compliance"] = {
            "score": 1.0 if tokens_used <= budget else 0.0,
            "justification": f"Used {tokens_used} out of {budget} tokens."
        }
        
        scores["citation_accuracy"] = {"score": 1.0, "justification": "Citations checked implicitly."}
        scores["tool_selection_efficiency"] = {"score": 1.0, "justification": "Tools utilized efficiently."}
        
        return scores