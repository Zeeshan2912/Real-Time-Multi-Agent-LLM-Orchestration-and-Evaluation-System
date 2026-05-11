CREATE TABLE IF NOT EXISTS evaluation_runs (
    id SERIAL PRIMARY KEY, 
    job_id TEXT UNIQUE, 
    test_case_id TEXT,
    exact_prompts JSONB, 
    tool_calls_log JSONB, 
    agent_outputs JSONB,
    scores JSONB, 
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS prompt_rewrites (
    id SERIAL PRIMARY KEY,
    rewrite_id TEXT UNIQUE,
    original_prompt TEXT,
    proposed_rewrite TEXT,
    approval_status TEXT DEFAULT 'pending',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);