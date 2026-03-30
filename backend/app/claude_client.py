import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load env from backend/.env
load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL","claude-sonnet-4-5-20250929")
DEFAULT_MAX_TOKENS = int(os.getenv("MAX_TOKEN", "2000"))
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

def call_claude(prompt:str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY in environment")
    
    client = Anthropic(api_key = api_key)

    resp = client.messages.create(
        model = DEFAULT_MODEL,
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        messages=[{"role":"user","content":prompt}],   
    )

    out = []
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            out.append(block.text)

    return "\n".join(out).strip()