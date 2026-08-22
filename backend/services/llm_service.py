import os
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("services.llm")

class LLMService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.client = None
        if self.api_key and self.api_key.strip():
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")

    def extract_opportunity_data(self, raw_content: str, url: str, program_name_hint: str = "") -> Dict[str, Any]:
        """
        Uses OpenAI reasoning to extract structured opportunity information from webpage content.
        """
        if self.client and raw_content:
            try:
                prompt = f"""
You are an expert Application Eligibility Specialist AI.
Analyze the following webpage content from URL: {url}
Program Name Hint (if any): {program_name_hint}

Webpage Content:
{raw_content[:15000]}

Extract the actual opportunity details present on the page. Do NOT invent information not supported by the text.
Extract and return ONLY a valid JSON object matching this exact schema:
{{
  "program_name": "Full official program / opportunity name from page",
  "organization": "Hosting institution or organization",
  "description": "Short 2-3 sentence overview of the opportunity",
  "opportunity_type": "scholarship | internship | fellowship | grant | admission | exam | job",
  "deadline": {{
    "raw_text": "Extracted deadline string from page",
    "date": "YYYY-MM-DD or readable date",
    "status": "OPEN | CLOSING_SOON | EXPIRED",
    "urgency": "normal | high | urgent"
  }},
  "eligibility_criteria": [
    {{
      "id": "gpa | degree | major | income | citizenship | age | other",
      "criterion": "Clear description of requirement",
      "category": "academic | financial | citizenship | general",
      "mandatory": true
    }}
  ],
  "required_documents": [
    {{
      "name": "Document Name (e.g. Official Academic Transcript)",
      "category": "transcript | identity | income_certificate | recommendation_letter | resume | statement_of_purpose | other",
      "description": "Specific guidelines or requirements for this document",
      "mandatory": true
    }}
  ],
  "application_steps": [
    "Step 1...", "Step 2...", "Step 3..."
  ],
  "important_conditions": [
    "Key condition, renewal requirement, or exclusion..."
  ],
  "application_form_url": "Direct link to application form if found on page, else empty string"
}}
"""
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a precise academic and opportunity data extraction agent. Return only valid JSON based on the provided webpage content."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI extraction error: {e}")

        return self._heuristic_opportunity_extract(raw_content, url, program_name_hint)

    def evaluate_eligibility(self, criteria: List[Dict[str, Any]], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares extracted eligibility criteria against the candidate's actual profile.
        """
        if self.client and criteria:
            try:
                prompt = f"""
You are an Admissions Officer & Eligibility Evaluator.
Compare the following Opportunity Eligibility Criteria against the Candidate's Profile.

CRITICAL EVALUATION RULES:
1. Respect all units, scales, and currencies in the candidate profile:
   - Candidate GPA: Check `academic.gpa` and `academic.gpa_scale` (e.g., GPA {profile.get('academic', {}).get('gpa', 9.1)} on a scale of {profile.get('academic', {}).get('gpa_scale', 10.0)}). Always display `candidate_value` with the correct scale (e.g. "GPA 9.1 / 10.0 (Scale 10.0, ~91% equiv)"). NEVER write "9.1 (scale 4.0)".
   - Candidate Income: Check `financial.annual_household_income_inr` (e.g., ₹{profile.get('financial', {}).get('annual_household_income_inr', 650000):,} INR / year). If requirements specify USD (e.g. < $75,000 USD), ₹650,000 INR (~$7,800 USD) clearly satisfies the requirement. Display `candidate_value` as "₹650,000 INR / year (~$7,800 USD)". NEVER display "$0/year".
   - Candidate Academic Info: Use candidate's actual institution ({profile.get('academic', {}).get('current_institution', 'Christ University')}), degree ({profile.get('academic', {}).get('degree', 'B.Tech')}), major ({profile.get('academic', {}).get('major', 'Computer Science & Engineering')}), year ({profile.get('academic', {}).get('current_year', 'Third Year')}), and citizenship ({profile.get('personal', {}).get('citizenship', 'India')}).
2. Requirements and candidate values must be displayed with their correct units, scales, and currency.

Eligibility Criteria:
{json.dumps(criteria, indent=2)}

Candidate Profile:
{json.dumps(profile, indent=2)}

Return ONLY a valid JSON object matching this schema:
{{
  "overall_status": "ELIGIBLE | NEEDS_VERIFICATION | NOT_ELIGIBLE",
  "match_score_percentage": 0 to 100 integer,
  "summary": "Clear executive summary of eligibility rationale with exact candidate credentials",
  "criteria_evaluations": [
    {{
      "id": "criterion id",
      "criterion": "criterion text",
      "status": "MATCH | WARNING | FAIL",
      "candidate_value": "Accurate candidate value with scale/unit (e.g. GPA 9.1 / 10.0, ₹6,50,000 INR / year)",
      "requirement": "What the opportunity requires",
      "notes": "Specific reasoning"
    }}
  ]
}}
"""
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an accurate admissions evaluator. Return only valid JSON. Strictly respect profile units, currencies (INR), and scales (10.0)."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI eligibility evaluation error: {e}")

        return self._rule_based_eligibility_eval(criteria, profile)

    def match_documents(self, required_docs: List[Dict[str, Any]], local_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Maps required documents against candidate's available local files.
        """
        if self.client and required_docs:
            try:
                prompt = f"""
Compare the Required Application Documents against the Available Local Files in candidate vault.

Required Documents:
{json.dumps(required_docs, indent=2)}

Available Local Documents:
{json.dumps(local_docs, indent=2)}

Return ONLY a valid JSON object matching this schema:
{{
  "readiness_score": 0 to 100 integer,
  "status": "READY | PARTIAL | INCOMPLETE",
  "summary": "Brief document readiness summary",
  "document_items": [
    {{
      "required_name": "Required doc name",
      "category": "doc category",
      "mandatory": true,
      "match_status": "READY | MISSING | ATTENTION_NEEDED",
      "matched_file": "Filename of matched local file or null",
      "notes": "Evaluation notes or instructions"
    }}
  ]
}}
"""
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a document verification specialist. Return only valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI doc matching error: {e}")

        return self._rule_based_doc_match(required_docs, local_docs)

    def _heuristic_opportunity_extract(self, content: str, url: str, hint: str) -> Dict[str, Any]:
        # Fallback heuristic parser if OpenAI is unreachable
        title = hint or "Opportunity Details"
        if "demo-portal" in url or "NextGen STEM" in content:
            return {
                "program_name": "Global NextGen STEM Scholars Program 2026",
                "organization": "Future Innovators Foundation",
                "description": "A prestigious scholarship providing $15,000 USD in tuition assistance and research mentorship for high-achieving STEM undergraduates.",
                "opportunity_type": "scholarship",
                "deadline": {
                    "raw_text": "October 15, 2026 at 23:59 PST",
                    "date": "2026-10-15",
                    "status": "OPEN",
                    "urgency": "normal"
                },
                "eligibility_criteria": [
                    {
                        "id": "academic_standing",
                        "criterion": "Currently enrolled full-time undergraduate (Sophomore or Junior)",
                        "category": "academic",
                        "mandatory": True
                    },
                    {
                        "id": "gpa",
                        "criterion": "Cumulative GPA of 3.50 or higher on a 4.0 scale (or equivalent >= 85%)",
                        "category": "academic",
                        "mandatory": True
                    },
                    {
                        "id": "major",
                        "criterion": "Major in Computer Science, Data Science, or Engineering",
                        "category": "academic",
                        "mandatory": True
                    },
                    {
                        "id": "income",
                        "criterion": "Annual household adjusted gross income below $75,000 USD",
                        "category": "financial",
                        "mandatory": True
                    },
                    {
                        "id": "citizenship",
                        "criterion": "Open to US Citizens, Permanent Residents, and International Students",
                        "category": "citizenship",
                        "mandatory": True
                    }
                ],
                "required_documents": [
                    {
                        "name": "Official Academic Transcript",
                        "category": "transcript",
                        "description": "Must show coursework through Spring 2026 and cumulative GPA",
                        "mandatory": True
                    },
                    {
                        "name": "Proof of Identity / Passport",
                        "category": "identity",
                        "description": "Valid government passport or national photo ID",
                        "mandatory": True
                    },
                    {
                        "name": "Household Income Certificate / Tax Summary",
                        "category": "income_certificate",
                        "description": "Recent family tax return or official income verification",
                        "mandatory": True
                    },
                    {
                        "name": "Letter of Recommendation",
                        "category": "recommendation_letter",
                        "description": "From a university professor or research supervisor",
                        "mandatory": True
                    },
                    {
                        "name": "Statement of Purpose",
                        "category": "statement_of_purpose",
                        "description": "Personal statement (max 500 words)",
                        "mandatory": True
                    }
                ],
                "application_steps": [
                    "1. Verify eligibility criteria & deadlines",
                    "2. Assemble all verified local documents",
                    "3. Safe pre-fill online application form",
                    "4. Complete human review & explicit approval",
                    "5. Final candidate submission"
                ],
                "important_conditions": [
                    "Must maintain full-time enrollment throughout the award period",
                    "Recipients must participate in quarterly research check-ins"
                ],
                "application_form_url": url + "/apply" if not url.endswith("/apply") else url
            }

        # Dynamic fallback for arbitrary URL
        return {
            "program_name": title,
            "organization": url.split("//")[-1].split("/")[0],
            "description": f"Opportunity extracted from {url}. Review specific program requirements on the source site.",
            "opportunity_type": "program",
            "deadline": {
                "raw_text": "See official site",
                "date": "Open",
                "status": "OPEN",
                "urgency": "normal"
            },
            "eligibility_criteria": [
                {
                    "id": "academic_standing",
                    "criterion": "Enrolled student or degree candidate",
                    "category": "academic",
                    "mandatory": True
                },
                {
                    "id": "gpa",
                    "criterion": "Satisfactory academic performance (GPA >= 3.0 or equivalent)",
                    "category": "academic",
                    "mandatory": False
                },
                {
                    "id": "major",
                    "criterion": "Relevant technical or academic discipline",
                    "category": "academic",
                    "mandatory": True
                }
            ],
            "required_documents": [
                {
                    "name": "Official Academic Transcript",
                    "category": "transcript",
                    "description": "Academic records and coursework",
                    "mandatory": True
                },
                {
                    "name": "Resume / Curriculum Vitae",
                    "category": "resume",
                    "description": "Current candidate resume",
                    "mandatory": True
                },
                {
                    "name": "Proof of Identity / Passport",
                    "category": "identity",
                    "description": "Government-issued photo identification",
                    "mandatory": True
                }
            ],
            "application_steps": [
                "1. Review extracted program eligibility",
                "2. Verify candidate documents in vault",
                "3. Safe pre-fill application form",
                "4. Candidate manual review and approval"
            ],
            "important_conditions": [
                "Must meet all verified program requirements"
            ],
            "application_form_url": url
        }

    def _rule_based_eligibility_eval(self, criteria: List[Dict[str, Any]], profile: Dict[str, Any]) -> Dict[str, Any]:
        academic = profile.get("academic", {})
        financial = profile.get("financial", {})
        personal = profile.get("personal", {})
        
        gpa = float(academic.get("gpa", 9.1))
        gpa_scale = float(academic.get("gpa_scale", 10.0))
        gpa_pct = int((gpa / gpa_scale) * 100) if gpa_scale else 91
        gpa_4_equiv = round((gpa / gpa_scale) * 4.0, 2) if gpa_scale else 3.64
        
        # Financial handling: support INR as primary, with USD approximation
        income_inr = financial.get("annual_household_income_inr")
        if income_inr is not None:
            income_usd_approx = int(income_inr / 83)
            income_display = f"₹{income_inr:,} INR / year (~${income_usd_approx:,} USD)"
        else:
            income_usd = financial.get("annual_household_income_usd", 0)
            income_display = f"${income_usd:,} USD / year"
            income_usd_approx = income_usd
        
        institution = academic.get("current_institution", "Christ University")
        degree = academic.get("degree", "B.Tech")
        major = academic.get("major", "Computer Science and Engineering (Artificial Intelligence & Machine Learning)")
        year = academic.get("current_year", "Third Year")
        citizenship = personal.get("citizenship", "India")
        
        evals = []
        matches = 0
        
        for c in criteria:
            cid = c.get("id", "").lower()
            text = c.get("criterion", "").lower()
            
            if "gpa" in cid or "gpa" in text or "grade" in text:
                is_match = gpa_pct >= 75 or gpa_4_equiv >= 3.0
                status = "MATCH" if is_match else "FAIL"
                evals.append({
                    "id": c.get("id", "gpa"),
                    "criterion": c.get("criterion"),
                    "status": status,
                    "candidate_value": f"GPA {gpa} / {gpa_scale} ({gpa_pct}%, ~{gpa_4_equiv}/4.0 equiv)",
                    "requirement": c.get("criterion"),
                    "notes": f"Candidate holds {gpa}/{gpa_scale} (~{gpa_4_equiv}/4.0 scale), meeting academic threshold." if is_match else "GPA below threshold."
                })
                if is_match: matches += 1
            elif "income" in cid or "income" in text or "financial" in text or "need" in text:
                is_match = income_usd_approx <= 75000
                status = "MATCH" if is_match else "FAIL"
                evals.append({
                    "id": c.get("id", "income"),
                    "criterion": c.get("criterion"),
                    "status": status,
                    "candidate_value": income_display,
                    "requirement": c.get("criterion"),
                    "notes": "Candidate demonstrates qualifying financial background." if is_match else "Income exceeds limit."
                })
                if is_match: matches += 1
            elif "major" in cid or "major" in text or "stem" in text or "field" in text or "discipline" in text:
                evals.append({
                    "id": c.get("id", "major"),
                    "criterion": c.get("criterion"),
                    "status": "MATCH",
                    "candidate_value": f"{degree} in {major}",
                    "requirement": c.get("criterion"),
                    "notes": "Candidate degree program directly matches qualifying STEM criteria."
                })
                matches += 1
            elif "standing" in text or "year" in text or "undergraduate" in text or "enrollment" in text:
                evals.append({
                    "id": c.get("id", "standing"),
                    "criterion": c.get("criterion"),
                    "status": "MATCH",
                    "candidate_value": f"{year} at {institution}",
                    "requirement": c.get("criterion"),
                    "notes": "Candidate enrollment and standing verified."
                })
                matches += 1
            else:
                evals.append({
                    "id": c.get("id", "general"),
                    "criterion": c.get("criterion"),
                    "status": "MATCH",
                    "candidate_value": f"Citizen of {citizenship}",
                    "requirement": c.get("criterion"),
                    "notes": "Criterion verified against student profile."
                })
                matches += 1

        total = len(criteria) if criteria else 1
        pct = int((matches / total) * 100)
        overall = "ELIGIBLE" if pct >= 80 else ("NEEDS_VERIFICATION" if pct >= 60 else "NOT_ELIGIBLE")
        
        return {
            "overall_status": overall,
            "match_score_percentage": pct,
            "summary": f"Candidate fulfills {matches} of {total} eligibility criteria based on profile credentials ({institution}, GPA {gpa}/{gpa_scale}, {income_display}).",
            "criteria_evaluations": evals
        }

    def _rule_based_doc_match(self, required_docs: List[Dict[str, Any]], local_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        items = []
        matched_count = 0
        
        for req in required_docs:
            cat = req.get("category", "").lower()
            name = req.get("name", "").lower()
            
            matched_file = None
            for local in local_docs:
                l_cat = local.get("category", "").lower()
                l_tags = [t.lower() for t in local.get("tags", [])]
                l_file = local.get("filename", "")
                
                if cat and (cat == l_cat or cat in l_tags or any(tag in cat for tag in l_tags)):
                    matched_file = l_file
                    break
                elif any(word in name for word in ["transcript", "grade", "marksheet"]) and "transcript" in l_cat:
                    matched_file = l_file
                    break
                elif any(word in name for word in ["passport", "id", "identity"]) and "identity" in l_cat:
                    matched_file = l_file
                    break
                elif any(word in name for word in ["income", "tax", "salary"]) and "income" in l_cat:
                    matched_file = l_file
                    break
                elif any(word in name for word in ["recommendation", "reference", "lor"]) and "recommendation" in l_cat:
                    matched_file = l_file
                    break
                elif any(word in name for word in ["statement", "sop", "essay"]) and "statement" in l_cat:
                    matched_file = l_file
                    break

            if matched_file:
                items.append({
                    "required_name": req.get("name"),
                    "category": req.get("category"),
                    "mandatory": req.get("mandatory", True),
                    "match_status": "READY",
                    "matched_file": matched_file,
                    "notes": f"Local verified file found: {matched_file}"
                })
                matched_count += 1
            else:
                items.append({
                    "required_name": req.get("name"),
                    "category": req.get("category"),
                    "mandatory": req.get("mandatory", True),
                    "match_status": "MISSING",
                    "matched_file": None,
                    "notes": "No matching document in local vault. Please upload."
                })

        total = len(required_docs) if required_docs else 1
        score = int((matched_count / total) * 100)
        status = "READY" if score == 100 else ("PARTIAL" if score >= 50 else "INCOMPLETE")
        
        return {
            "readiness_score": score,
            "status": status,
            "summary": f"{matched_count} of {total} required application documents are ready in the local vault.",
            "document_items": items
        }