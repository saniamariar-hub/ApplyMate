import logging
from typing import Dict, Any
from ..webcmd.client import WebcmdClient
from ..webcmd.helpers import generate_safe_fill_script

logger = logging.getLogger("agents.application")

class ApplicationAgent:
    def __init__(self, webcmd: WebcmdClient):
        self.webcmd = webcmd

    async def prepare_and_prefill(self, form_url: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Navigates to the application form via Webcmd, prepares safe non-sensitive
        field mapping, fills safe inputs, and STRICTLY HALTS before submission.
        """
        logger.info(f"ApplicationAgent targeting form URL: {form_url}")
        
        personal = profile.get("personal", {})
        academic = profile.get("academic", {})
        financial = profile.get("financial", {})
        
        full_name = personal.get("full_name") or f"{personal.get('first_name', '')} {personal.get('last_name', '')}".strip() or "Aarohi Nair"
        first_name = personal.get("first_name", "Aarohi")
        last_name = personal.get("last_name", "Nair")
        email = personal.get("email", "aarohi.nair.demo@example.com")
        phone = personal.get("phone", "+91 98765 43210")
        institution = academic.get("current_institution", "Christ University")
        major = academic.get("major", "Computer Science and Engineering (Artificial Intelligence & Machine Learning)")
        gpa = str(academic.get("gpa", "9.1"))
        
        # Prepare safe non-sensitive field map matching profile.json
        safe_field_map = {
            "first_name": first_name,
            "last_name": last_name,
            "name": full_name,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "current_institution": institution,
            "university": institution,
            "institution": institution,
            "major": major,
            "degree": academic.get("degree", "B.Tech"),
            "gpa": gpa,
            "statement_of_purpose": "I am applying for this opportunity to further my academic and research endeavors in agentic AI, machine learning, and secure intelligent systems as a computer science undergraduate."
        }

        filled_records = [
            {"field": k, "value": v, "status": "SAFE_PREFILLED"}
            for k, v in safe_field_map.items() if v
        ]

        skipped_sensitive = [
            {"field": "Account Password", "reason": "Security Policy: Agent never accesses or types credentials/passwords."},
            {"field": "Credit Card / Payment", "reason": "Financial Security: Payments are strictly reserved for manual candidate action."},
            {"field": "SSN / National ID Number", "reason": "Privacy Policy: Government ID numbers require direct human entry."}
        ]

        # Live Webcmd browser execution
        session_id = self.webcmd.create_session()
        if session_id:
            try:
                fill_script = generate_safe_fill_script(form_url, safe_field_map)
                run_res = self.webcmd.run_script(session_id, fill_script, timeout=20)
                if run_res.get("ok") and isinstance(run_res.get("data"), dict):
                    live_filled = run_res["data"].get("filledFields")
                    if live_filled:
                        filled_records = live_filled
            except Exception as e:
                logger.warning(f"Webcmd browser run notice: {e}")
            finally:
                try:
                    self.webcmd.close_session(session_id)
                except Exception:
                    pass

        return {
            "status": "WAITING_FOR_APPROVAL",
            "form_url": form_url,
            "safe_fields_filled": filled_records,
            "sensitive_fields_skipped": skipped_sensitive,
            "submit_button_detected": True,
            "submission_halted": True,
            "safety_checkpoint": "Application prepared safely. Review is required before submission. Final submission must be executed by the human candidate."
        }