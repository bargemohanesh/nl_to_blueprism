from pydantic import BaseModel
from typing import Optional

class NLToBPRequest(BaseModel):
    process_description: str
    include_xml: bool = True

class NLToBPResponse(BaseModel):
    process_name: str
    bp_mapping: str
    xml_skeleton: Optional[str] = None