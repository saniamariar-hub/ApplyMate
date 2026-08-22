# 🎓 Application Readiness Agent (Hackathon MVP)

> **Autonomous Browser Agent Copilot for Scholarships, Internships, Fellowships & University Applications**  
> Powered by **Webcmd 0.7.4** browser automation, **OpenAI** structured reasoning, local student credential verification, and a mandatory **Human Approval Safety Guardrail**.

---

## 🌟 Key Highlights

- **Real Webcmd 0.7.4 Browser Engine**: Drives real web pages with accessibility snapshots (`webcmd browser snapshot`) and Playwright execution in QuickJS (`webcmd browser run`).
- **Lightweight 4-Agent Architecture**: Clean, deterministic separation of concerns across Orchestrator, Eligibility, Document, and Application agents without bloated frameworks.
- **Strict Human Approval Checkpoint**: Automatically identifies and safely pre-fills non-sensitive fields, but **strictly halts before submission**. Automated submission is prohibited.


---

## 🏛 Architecture

```
                                  +---------------------------------------+
                                  |    React + Vite Dashboard (:5173)     |
                                  +---------------------------------------+
                                                     |
                                                     | (SSE Stream / REST)
                                                     v
                                  +---------------------------------------+
                                  |      Orchestrator Agent (FastAPI)     |
                                  +---------------------------------------+
                                    /                 |                 \
                                   /                  |                  \
                                  v                   v                   v
              +----------------------+   +----------------------+   +----------------------+
              |  Eligibility Agent   |   |    Document Agent    |   |  Application Agent   |
              |  (OpenAI + Webcmd)   |   |  (Vault Doc Matcher) |   |  (Webcmd Safe Fill)  |
              +----------------------+   +----------------------+   +----------------------+
                         |                          |                          |
                         v                          v                          v
             [Webcmd 0.7.4 Web Fetch]        [demo_data/docs/]       [Webcmd Browser Runtime]
                         |                                                     |
                         v                                                     v
             [Target Opportunity Web]                                [Safe Fields Populated]
                                                                               |
                                                                               v
                                                                 🟡 [HUMAN APPROVAL CHECKPOINT]
```

---

## 📦 Project Structure

```
application-readiness-agent/
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py        # Workflow state machine & SSE progress streaming
│   │   ├── eligibility_agent.py   # Researches URL & extracts requirements via OpenAI
│   │   ├── document_agent.py      # Cross-references vault documents against required files
│   │   └── application_agent.py   # Navigates form & pre-fills safe fields via Webcmd
│   ├── webcmd/
│   │   ├── client.py              # Official Webcmd 0.7.4 CLI & browser session wrapper
│   │   └── helpers.py             # Playwright scripts for DOM inspection & safe filling
│   ├── services/
│   │   ├── profile_service.py     # Student demo profile loader & editor
│   │   ├── llm_service.py         # OpenAI structured JSON extractor & evaluator
│   │   └── mock_portal.py         # Built-in live scholarship portal (/demo-portal)
│   ├── main.py                    # FastAPI application server
│   └── requirements.txt           # Python backend dependencies
├── demo_data/
│   ├── profile.json               # Demo student profile (Alex Rivera, 3.85 GPA)
│   └── documents/                 # Sample verified PDFs & text records
│       ├── academic_transcript_official.pdf
│       ├── identity_proof_passport.pdf
│       ├── income_certificate_2025.pdf
│       ├── recommendation_letter_prof_smith.pdf
│       ├── resume_alex_rivera.pdf
│       ├── statement_of_purpose_draft.txt
│       └── demo_documents_index.json
├── frontend/                      # React + Vite + Tailwind CSS dashboard
│   ├── src/
│   │   ├── components/            # Visual workflow progress, cards & approval modal
│   │   ├── App.jsx                # Main dashboard UI
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── .gitignore
├── start.bat                      # 1-click startup script for Windows
├── run_backend.bat                # Start backend only
├── run_frontend.bat               # Start frontend only
└── README.md
```

---

## 🚀 Quick Start (Windows Setup)

### 1. Prerequisites
- **Node.js**: v18+ (tested on Node.js 24.13.0)
- **Python**: 3.10+ (tested on Python 3.13)
- **Webcmd**: 0.7.4 (`npm install -g @agentrhq/webcmd`)
- **Google Chrome** installed at default location (`C:\Program Files\Google\Chrome\Application\chrome.exe`)

### 2. Environment Configuration
Create `.env` in the root directory:
```bash
copy .env.example .env
```
Edit `.env` and supply your OpenAI API key:
```ini
OPENAI_API_KEY=sk-proj-your-openai-key-here
CLOAKBROWSER_BINARY_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

### 3. Install Dependencies

**Backend:**
```bash
python -m pip install -r backend/requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 4. Run Application (1-Click Start)
Double-click `start.bat` or run:
```powershell
.\start.bat
```

Or run manually in separate terminals:
- **Backend (Terminal 1)**:
  ```powershell
  python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
  ```
- **Frontend (Terminal 2)**:
  ```powershell
  cd frontend
  npm run dev
  ```

---

## 🎯 Verification & Testing

Open `http://localhost:5173` in your browser:
1. Click the quick-pick preset **Global NextGen STEM Scholars Program 2026** (or enter any public URL).
2. Click **Analyze Application Readiness**.
3. Watch the real-time agent workflow stream:
   - `[✓]` Webcmd connects and fetches the target portal.
   - `[✓]` Eligibility Agent extracts criteria, deadline, and conditions.
   - `[✓]` Document Agent evaluates local vault files against requirements.
   - `[✓]` Application Agent navigates to application form and safe fills inputs.
   - `[🟡]` **Safety Guard halts pipeline at Waiting for Human Approval**.
4. Click **Review & Approve Readiness** to confirm human verification.

---

## 🛡 Safety & Anti-Hallucination Guarantees

1. **Strict Submission Blocker**: The agent is programmatically restricted from submitting forms or entering financial/credential data.
2. **Zero Faked Browser Actions**: Every interaction routes through real Webcmd CLI commands with diagnostic exit codes and logs.
3. **Graceful Fallbacks**: If a website is slow or structurally altered, the agent inspects alternative DOM handles and reports the exact halt reason.
