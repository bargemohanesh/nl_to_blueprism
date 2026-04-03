from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML_PAGE = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>NL → Blue Prism Generator (POC)</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; max-width: 1100px; }
    textarea { width: 100%; height: 180px; font-family: Consolas, monospace; }
    pre { background: #f6f6f6; padding: 12px; overflow-x: auto; white-space: pre-wrap; }
    .row { display: flex; gap: 16px; }
    .col { flex: 1; }
    button { padding: 10px 16px; cursor: pointer; margin-right: 8px; }
    label { display:block; margin: 10px 0 6px; font-weight: 600; }
  </style>
</head>
<body>
  <h2>NL → Blue Prism Generator (POC)</h2>

  <label>Process Description (Natural Language)</label>
  <textarea id="inp">Process Name: Helix DLP Whitelisting Search. Steps: 1) Search Helix for work orders with Support Category: DLP Whitelisting for EU-IC-CS - Endpoint Security. 2) If no WO numbers found, end process. 3) If WO found, return list of Work Order IDs and Request IDs. Systems Used: Helix ITSM (REST API).</textarea>

  <div style="margin-top:10px;">
    <label>
      <input type="checkbox" id="includeXml" checked/>
      Include XML
    </label>

    <button type="button" onclick="generate()">Generate</button>
    <button type="button" onclick="downloadMapping()">Download Mapping (.txt)</button>
    <button type="button" onclick="downloadXml()">Download XML (.xml)</button>
  </div>

  <div class="row" style="margin-top:16px;">
    <div class="col">
      <h3>Blue Prism Mapping</h3>
      <pre id="mapping"></pre>
    </div>
    <div class="col">
      <h3>XML skeleton</h3>
      <pre id="xml"></pre>
    </div>
  </div>

  <script>
    let lastProcessName = "bp_process";

    async function generate() {
      const mappingEl = document.getElementById("mapping");
      const xmlEl = document.getElementById("xml");

      mappingEl.textContent = "Generating...";
      xmlEl.textContent = "";

      const payload = {
        process_description: document.getElementById("inp").value,
        include_xml: document.getElementById("includeXml").checked
      };

      try {
        const res = await fetch("/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
          mappingEl.textContent = JSON.stringify(data, null, 2);
          return;
        }

        mappingEl.textContent = data.bp_mapping || "";
        xmlEl.textContent = data.xml_skeleton || "";

        // capture process name for better filenames
        lastProcessName = data.process_name || "bp_process";

      } catch (err) {
        mappingEl.textContent = "Client error: " + err;
      }
    }

    function downloadText(filename, text) {
      const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }

    function downloadMapping() {
      const mapping = document.getElementById("mapping").textContent || "";
      downloadText(`${lastProcessName}_mapping.txt`, mapping);
    }

    function downloadXml() {
      const xml = document.getElementById("xml").textContent || "";
      downloadText(`${lastProcessName}.bpprocess`, xml);  // change .xml to .bpprocess
    }
    
  </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE