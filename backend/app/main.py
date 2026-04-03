from fastapi import FastAPI, HTTPException
from app.schemas import NLToBPRequest, NLToBPResponse
from app.prompt_loader import build_final_prompt
from app.claude_client import call_claude
from app.ui import router as ui_router
import re
import uuid

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
    # Try complete fenced block first
    pattern = r"```xml\s*(.*?)\s*```"
    m = re.search(pattern, model_output, flags=re.DOTALL | re.IGNORECASE)
    if m:
        xml = m.group(1).strip()
        text_wo_xml = re.sub(pattern, "", model_output, count=1, flags=re.DOTALL | re.IGNORECASE).strip()
        return text_wo_xml, xml

    # Handle truncated XML — no closing ```
    pattern2 = r"```xml\s*(.*)"
    m2 = re.search(pattern2, model_output, flags=re.DOTALL | re.IGNORECASE)
    if m2:
        xml = m2.group(1).strip()
        if not xml.endswith("</process>"):
            # Remove incomplete/broken last stage tag
            xml = re.sub(r'<stage[^>]*$', '', xml, flags=re.DOTALL).strip()
            # Close any open stage tag
            if not xml.endswith("</stage>"):
                xml = xml + "\n  </stage>"
            xml = xml + "\n</process>"
        text_wo_xml = re.sub(pattern2, "", model_output, count=1, flags=re.DOTALL | re.IGNORECASE).strip()
        return text_wo_xml, xml

    # Fallback: raw <process ...> block
    pattern3 = r'(<process\b.*?</process>)'
    m3 = re.search(pattern3, model_output, flags=re.DOTALL | re.IGNORECASE)
    if m3:
        xml = m3.group(1).strip()
        text_wo_xml = model_output.replace(xml, "").strip()
        return text_wo_xml, xml

    return model_output.strip(), None

def replace_guids(xml: str) -> str:
    # Replace short stage IDs like s01, s02, p01
    short_id_pattern = r'\b(p01|s\d{2})\b'
    found_short = re.findall(short_id_pattern, xml)
    unique_short = list(dict.fromkeys(found_short))
    short_map = {s: str(uuid.uuid4()) for s in unique_short}
    for old, new in short_map.items():
        xml = re.sub(r'\b' + old + r'\b', new, xml)
    
    # Replace any remaining full UUIDs
    guid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    found = re.findall(guid_pattern, xml, flags=re.IGNORECASE)
    unique_guids = list(dict.fromkeys(found))
    guid_map = {g: str(uuid.uuid4()) for g in unique_guids}
    for old, new in guid_map.items():
        xml = xml.replace(old, new)
    return xml

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

        if xml:
            xml = replace_guids(xml)

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
    
