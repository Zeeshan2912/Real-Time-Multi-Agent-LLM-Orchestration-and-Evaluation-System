# AI Collaboration Attestation

As per the assignment allowances, this project was developed in close collaboration with an AI coding assistant (Google DeepMind's Antigravity / Gemini model).

## Where and How AI Was Used

1. **Architecture & Scaffolding**: 
   - AI was used to draft the initial boilerplate for FastAPI, SQLAlchemy asynchronous models, and the `docker-compose.yml` configuration.
   - The AI generated the `task.md` implementation plan and managed the state machine transition from mock stubs to actual implementation.
2. **LLM Integration**: 
   - AI assisted in integrating the `litellm` library and writing the JSON parsing wrappers (`app/utils/llm.py`) to ensure structured outputs.
3. **Evaluation Scaffolding**: 
   - The LLM-as-a-judge prompt templates inside `scorer.py` and the failure-case analytical prompts in `meta.py` were co-authored with AI to ensure edge cases were caught.

## Human & AI Synergies
The AI excelled at rapidly building out the Abstract Base Classes (e.g., the `ToolContract` with retry logic) and the topological sort algorithms (`decomposer.py`). The human (developer intent) guided the strict boundary enforcement, insisting that agents communicate *only* via the `AgentContext` object, ensuring the system strictly met the complex assignment constraints.
