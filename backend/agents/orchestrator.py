import asyncio
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, AsyncGenerator
from .eligibility_agent import EligibilityAgent
from .document_agent import DocumentAgent
from .application_agent import ApplicationAgent
from ..services.profile_service import ProfileService
from ..services.llm_service import LLMService
from ..webcmd.client import WebcmdClient

logger = logging.getLogger("agents.orchestrator")

class OrchestratorAgent:
    def __init__(self):
        self.webcmd = WebcmdClient()
        self.llm = LLMService()
        self.profile_service = ProfileService()
        
        self.eligibility_agent = EligibilityAgent(self.webcmd, self.llm)
        self.document_agent = DocumentAgent(self.llm)
        self.application_agent = ApplicationAgent(self.webcmd)
        
        self.workflows: Dict[str, Dict[str, Any]] = {}

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self.workflows.get(workflow_id, {"error": "Workflow not found"})

    def approve_workflow(self, workflow_id: str) -> Dict[str, Any]:
        wf = self.workflows.get(workflow_id)
        if not wf:
            return {"ok": False, "error": "Workflow not found"}
        
        wf["state"] = "APPROVED_BY_USER"
        wf["progress_pct"] = 100
        wf["approval_timestamp"] = datetime.now().isoformat()
        wf["logs"].append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "stage": "APPROVAL",
            "status": "APPROVED",
            "message": "Human approval granted. Candidate is cleared to inspect pre-filled form and submit."
        })
        return {"ok": True, "workflow": wf}

    async def execute_workflow(self, target_url: str, program_name: str) -> AsyncGenerator[Dict[str, Any], None]:
        workflow_id = str(uuid.uuid4())
        profile = self.profile_service.get_profile()

        state = {
            "workflow_id": workflow_id,
            "target_url": target_url,
            "program_name": program_name,
            "candidate_name": profile.get("personal", {}).get("full_name", "Aarohi Nair"),
            "state": "INITIALIZED",
            "progress_pct": 5,
            "created_at": datetime.now().isoformat(),
            "logs": [],
            "eligibility_data": None,
            "document_data": None,
            "application_data": None
        }
        self.workflows[workflow_id] = state

        def add_log(stage: str, message: str, status: str = "INFO"):
            entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "stage": stage,
                "status": status,
                "message": message
            }
            state["logs"].append(entry)
            return entry

        # 1. Start & Navigate
        state["state"] = "NAVIGATING_WEBSITE"
        state["progress_pct"] = 15
        add_log("WEBCMD_BROWSER", f"Inspecting target website {target_url} via Webcmd 0.7.4...", "RUNNING")
        yield state
        await asyncio.sleep(0.4)

        # 2. Extract Eligibility & Program Information
        state["state"] = "EXTRACTING_REQUIREMENTS"
        state["progress_pct"] = 40
        add_log("ELIGIBILITY_AGENT", "Extracting dynamic requirements, deadlines, and criteria with OpenAI reasoning...", "RUNNING")
        yield state

        try:
            elig_res = await self.eligibility_agent.analyze(target_url, program_name, profile)
            state["eligibility_data"] = elig_res
            add_log("ELIGIBILITY_AGENT", f"Extracted program: '{elig_res['program_info']['name']}'. Overall Status: {elig_res['eligibility_evaluation']['overall_status']}", "SUCCESS")
        except Exception as e:
            logger.error(f"Eligibility analysis notice: {e}")
            add_log("ELIGIBILITY_AGENT", f"Analysis error: {e}", "ERROR")

        state["progress_pct"] = 55
        yield state
        await asyncio.sleep(0.3)

        # 3. Check Documents
        state["state"] = "CHECKING_DOCUMENTS"
        state["progress_pct"] = 65
        add_log("DOCUMENT_AGENT", "Verifying required documents against student candidate vault...", "RUNNING")
        yield state

        try:
            req_docs = state["eligibility_data"].get("required_documents", []) if state["eligibility_data"] else []
            doc_res = await self.document_agent.verify_documents(req_docs)
            state["document_data"] = doc_res
            add_log("DOCUMENT_AGENT", f"Document readiness: {doc_res.get('readiness_score')}% ({doc_res.get('status')})", "SUCCESS")
        except Exception as e:
            logger.error(f"Document verification notice: {e}")
            add_log("DOCUMENT_AGENT", f"Document error: {e}", "ERROR")

        state["progress_pct"] = 75
        yield state
        await asyncio.sleep(0.3)

        # 4. Form Safe Pre-fill & Safety Boundary
        state["state"] = "PREPARING_APPLICATION"
        state["progress_pct"] = 85
        
        form_url = target_url
        if state["eligibility_data"] and state["eligibility_data"].get("program_info", {}).get("application_form_url"):
            form_url = state["eligibility_data"]["program_info"]["application_form_url"]
        elif not form_url.endswith("/apply") and "demo-portal" in form_url:
            form_url = form_url.rstrip("/") + "/apply"

        add_log("APPLICATION_AGENT", f"Navigating to application form at {form_url} via Webcmd...", "RUNNING")
        yield state

        try:
            app_res = await self.application_agent.prepare_and_prefill(form_url, profile)
            state["application_data"] = app_res
            add_log("APPLICATION_AGENT", f"Safe fields populated ({len(app_res.get('safe_fields_filled', []))} inputs). Sensitive fields protected.", "SUCCESS")
        except Exception as e:
            logger.error(f"Application prefill notice: {e}")
            add_log("APPLICATION_AGENT", f"Application notice: {e}", "ERROR")

        # 5. Mandatory Safety Stop - Application Prepared, Waiting for Human Approval
        state["state"] = "WAITING_FOR_APPROVAL"
        state["progress_pct"] = 90
        add_log("SAFETY_GUARD", "APPLICATION PREPARED: Form fields pre-filled safely. SUBMISSION HALTED: Explicit human approval is required before proceeding to submit.", "APPROVAL_REQUIRED")
        yield state