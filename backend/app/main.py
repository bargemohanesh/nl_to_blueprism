from fastapi import FastAPI, HTTPException
from app.schemas import NLToBPRequest, NLToBPResponse
from app.prompt_loader import build_final_prompt
from app.claude_client import call_claude
from app.ui import router as ui_router
import re

app = FastAPI(title = "NL to Blue Prism Generator", version="0.1")
app.include_router(ui_router)

def parse_process_name(model_output: str) -> str:
    """
    Extract process name from lines like:
    - Process name: Demo_process
    - ## Process Name: Demo_Process
    - Process name:\nDemo_Process
    """
    lines = [ln.strip() for ln in model_output.splitlines() if ln.strip()]

    # 1) Direct "process Name:" on same line 
    for ln in lines:
        m = re.match(r"^#+\s*Process\s*Name\s*:\s*(.+)$", ln, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
        m = re.match(r"^Process\s*Name\s*:\s*(.+)$",ln, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
        
    # 2) "Process Name:" then next non-empty line
    for i, ln in enumerate(lines[:-1]):
        if re.match(r"^#+\s*Process\s*Name\s*:\s*$", ln, flags=re.IGNORECASE) or \
           re.match(r"^Process\s*Name\s*:\s*$", ln, flags=re.IGNORECASE):
            return lines[i+1].strip()
        
    return "Unknown_Process"

def extract_xml_skeleton(model_output: str):
    """
    Extract XML skeleton from a fenced code block:
    ```xml
    ...
    ```
    Returns (text_without_xml_block, xml_or_none)
    """
    pattern = r"```xml\s*(.*?)\s*```"
    m = re.search(pattern, model_output, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return model_output.strip(), None
    
    xml = m.group(1).strip()
    # Remove only the first XML block
    text_wo_xml = re.sub(pattern, "", model_output, count=1, flags=re.DOTALL | re.IGNORECASE).strip()
    return text_wo_xml, xml

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate", response_model = NLToBPResponse)
def generate(req:NLToBPRequest):
    try:
        final_prompt = build_final_prompt(req.process_description)
        model_output = call_claude(final_prompt)

        process_name = parse_process_name(model_output)
        bp_text, xml = extract_xml_skeleton(model_output)

        return NLToBPResponse(
            process_name=process_name,
            bp_mapping=bp_text,
            xml_skeleton=xml if req.include_xml else None,
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(tb) # Show full stack trace in uvicorn console
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}") 