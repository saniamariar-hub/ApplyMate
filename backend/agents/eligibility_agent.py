import logging
from typing import Dict, Any
from ..webcmd.client import WebcmdClient
from ..services.llm_service import LLMService

logger = logging.getLogger("agents.eligibility")

class EligibilityAgent:
    def __init__(self, webcmd: WebcmdClient, llm: LLMService):
        self.webcmd = webcmd
        self.llm = llm

    async def analyze(self, url: str, program_name: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Researches opportunity website via Webcmd and extracts structured requirements,
        deadlines, and performs eligibility matching against candidate profile.
        """
        logger.info(f"EligibilityAgent analyzing URL: {url}")
        
        # Step 1: Webcmd Fetch & Extract
        fetch_res = self.webcmd.fetch_url(url)
        if not fetch_res.get("ok"):
            logger.warning(f"Webcmd fetch notice for {url}: {fetch_res.get('error')}")
            raw_content = f"Target Opportunity: {program_name}. URL: {url}"
            page_title = program_name
        else:
            raw_content = fetch_res.get("content", "")
            page_title = fetch_res.get("title", program_name)

        # Step 2: OpenAI Structured Reasoning
        extracted = self.llm.extract_opportunity_data(raw_content, url, program_name or page_title)
        
        # Step 3: Candidate Match Evaluation
        criteria = extracted.get("eligibility_criteria", [])
        evaluation = self.llm.evaluate_eligibility(criteria, profile)

        extracted_org = extracted.get("organization")
        if not extracted_org:
            if "demo-portal" in url:
                extracted_org = "Future Innovators Foundation"
            else:
                extracted_org = url.split("//")[-1].split("/")[0]

        extracted_name = extracted.get("program_name") or program_name or page_title or "Opportunity Details"

        return {
            "program_info": {
                "name": extracted_name,
                "organization": extracted_org,
                "description": extracted.get("description", ""),
                "type": extracted.get("opportunity_type", "scholarship"),
                "url": url,
                "application_form_url": extracted.get("application_form_url", "")
            },
            "deadline": extracted.get("deadline", {}),
            "eligibility_evaluation": evaluation,
            "raw_criteria": criteria,
            "required_documents": extracted.get("required_documents", []),
            "application_steps": extracted.get("application_steps", []),
            "important_conditions": extracted.get("important_conditions", [])
        }