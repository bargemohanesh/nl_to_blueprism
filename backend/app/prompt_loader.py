from pathlib import Path

# We are inside backend/app/, so project root is: backend/..
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROMPT_TXT = PROJECT_ROOT / "prompt.txt"
OUTPUT_FORMAT_MD = PROJECT_ROOT / "output_format.md"
EXAMPLE_MD = PROJECT_ROOT / "examples.md"

def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding = "utf-8").strip()

def build_final_prompt(user_process_description: str) -> str:
    """
    Builds one final prompt string for the LLM.
    
    IMPORTANT:
    - Chat models cannot read local files by path.
    - We must inject the content of prompt.txt, output_format.md, examples.md into the final prompt.
    """
    base_prompt = read_text(PROMPT_TXT)
    output_format = read_text(OUTPUT_FORMAT_MD)
    examples = read_text(EXAMPLE_MD)

    final_prompt = f"""{base_prompt}

OUTPUT FORMAT: 
{output_format}

FEW-SHOT EXAMPLES:
{examples}

STRICT OUTPUT CONTRACT (MUST FOLLOW):
- Output MUST be plain text only (no markdown headings like # or ##).
- Output MUST follow the exact sections and keys from OUTPUT FORMAT.
- Do NOT add extra sections like "Flow Diagram" or "Blue Prism Process Conversion.
- Use the exact lables: Process Name, Process Purspose, System used, Main Stages, Data Items, Exception Handling, XML skeleton.
- XML skeleton MUST be in a fenced code block starting with ```xml and ending with ```(so it can be parsed).
- If information is missing, write N/A but keep the keys.
- In XML skeleton, stageids MUST be short IDs like s01, s02, s03 — NOT full UUIDs
- preferredid in process tag MUST be p01 — NOT a full UUID

NOW CONVERT THIS PROCESS (Natural Language):
{user_process_description}
"""
    return final_prompt