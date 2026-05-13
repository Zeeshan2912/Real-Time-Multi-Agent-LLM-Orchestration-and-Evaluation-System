import litellm
import json
import re
from app.config import settings
import logging

async def generate_text(prompt: str, system_prompt: str = "You are a helpful AI.", temperature=None) -> str:
    temp = temperature if temperature is not None else settings.LLM_TEMPERATURE
    try:
        response = await litellm.acompletion(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"LLM Error: {e}")
        return ""

async def generate_json(prompt: str, system_prompt: str = "You must output valid JSON.", schema=None) -> dict:
    try:
        if schema:
            system_prompt += f"\n\nEnsure the JSON strictly adheres to this schema:\n{json.dumps(schema)}"
        
        response = await litellm.acompletion(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        content = response.choices[0].message.content
        # Extract JSON from markdown block if present
        match = re.search(r'```(?:json)?(.*?)```', content, re.DOTALL)
        if match:
            content = match.group(1).strip()
        return json.loads(content)
    except Exception as e:
        logging.error(f"LLM JSON Error: {e}")
        return {}
