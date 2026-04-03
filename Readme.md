# NL → Blue Prism Generator (POC)

An AI-powered tool that converts **Natural Language process descriptions** into **Blue Prism-compatible process definitions** — including stage mapping and importable `.bpprocess` XML files.

Built with **FastAPI** + **Claude AI (Anthropic)**.

---

## What It Does

1. Takes a plain English description of an RPA process
2. Generates a structured **Blue Prism stage mapping** (process name, stages, data items, exception handling)
3. Generates a **`.bpprocess` XML file** importable directly into Blue Prism Studio v7.5
4. Provides a simple web UI to generate, view, and download outputs

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10, FastAPI, Uvicorn |
| AI Model | Claude Sonnet (Anthropic API) |
| Frontend | HTML/JS (served via FastAPI) |
| Output Format | Blue Prism v7.5 `.bpprocess` XML |

---

## Project Structure

```
nl_to_blueprism/
├── backend/
│   └── app/
│       ├── main.py           # FastAPI app, XML parsing, GUID replacement
│       ├── claude_client.py  # Anthropic API client
│       ├── prompt_loader.py  # Builds final prompt from files
│       ├── schemas.py        # Pydantic request/response models
│       └── ui.py             # Web UI (HTML served via FastAPI)
├── prompt.txt                # System prompt + BP generation rules
├── output_format.md          # Output structure template
├── examples.md               # Few-shot examples for the model
├── requirements.txt
└── .env                      # API key (not committed to git)
```

---

## Prerequisites

- Python 3.10+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- Blue Prism v7.5 (for importing generated files)

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/nl-to-blueprism.git
cd nl-to-blueprism
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```
ANTHROPIC_API_KEY=your_api_key_here
MODEL=claude-sonnet-4-5-20250929
MAX_TOKEN=8000
TEMPERATURE=0
```

**5. Run the server**
```bash
cd backend
uvicorn app.main:app --reload
```

**6. Open in browser**
```
http://127.0.0.1:8000
```

---

## How to Use

1. Enter a process description in plain English in the text area
2. Check **Include XML** checkbox
3. Click **Generate**
4. View the **Blue Prism Mapping** (left panel) and **XML skeleton** (right panel)
5. Click **Download XML (.bpprocess)** to save the file
6. In **Blue Prism client** → **File → Import → Process/Object** → select the `.bpprocess` file
7. Open the imported process in **Process Studio** to view the staging diagram

---

## Example Input

```
Process Name: AD_Password_Reset. Steps:
1) Get ticket details from ServiceNow.
2) Login to Active Directory.
3) Search for user by username.
4) If user found, reset password and update ticket as resolved.
5) If user not found, update ticket as failed.
System Used: ServiceNow, Active Directory.
```

---

## Known Limitations

- Generated XML is a **structural skeleton** — business logic, inputs/outputs, and expressions must be configured manually in BP Studio
- Process locking in BP Studio may occur if a previously imported process was not closed before re-importing
- Processes with loops use `type="Action"` for LoopStart/LoopEnd stages due to BP import format constraints

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| POST | `/generate` | Generate BP mapping + XML |

### POST /generate

**Request:**
```json
{
  "process_description": "Your NL process description here",
  "include_xml": true
}
```

**Response:**
```json
{
  "process_name": "Process_Name",
  "bp_mapping": "Stage mapping text...",
  "xml_skeleton": "<process>...</process>"
}
```

---

## Deployment (Render / Railway)

1. Push code to GitHub
2. Create new web service on [Render](https://render.com) or [Railway](https://railway.app)
3. Set environment variables:
   - `ANTHROPIC_API_KEY`
   - `MODEL`
   - `MAX_TOKEN`
   - `TEMPERATURE`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Share the generated URL with your team

---

## Author

**Mohanesh Barge**  
AI Engineer | Sony India Software Centre  
[LinkedIn](https://www.linkedin.com/in/mohanesh-barge) | [GitHub](https://github.com/bargemohanesh)
