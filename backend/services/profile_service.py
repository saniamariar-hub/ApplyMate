import os
import json
from typing import Dict, Any, Optional

class ProfileService:
    def __init__(self, profile_path: Optional[str] = None):
        if profile_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.profile_path = os.path.join(base_dir, "demo_data", "profile.json")
        else:
            self.profile_path = profile_path

    def get_profile(self) -> Dict[str, Any]:
        if not os.path.exists(self.profile_path):
            return {}
        try:
            with open(self.profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to read profile: {e}"}

    def save_profile(self, new_data: Dict[str, Any]) -> bool:
        try:
            os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=2)
            return True
        except Exception:
            return False

    def get_profile_summary(self) -> str:
        p = self.get_profile()
        if not p:
            return "No profile found."
        personal = p.get("personal", {})
        academic = p.get("academic", {})
        financial = p.get("financial", {})
        
        gpa = academic.get("gpa", "9.1")
        gpa_scale = academic.get("gpa_scale", "10.0")
        
        income_inr = financial.get("annual_household_income_inr")
        if income_inr is not None:
            income_str = f"₹{income_inr:,} INR / year (~${int(income_inr/83):,} USD)"
        else:
            income_usd = financial.get("annual_household_income_usd", 0)
            income_str = f"${income_usd:,} USD / year"
        
        return f"""
Candidate Name: {personal.get('full_name', 'Aarohi Nair')}
Email: {personal.get('email', 'aarohi.nair.demo@example.com')}
Phone: {personal.get('phone', '+91 98765 43210')}
Age: {personal.get('age', 22)}
Citizenship: {personal.get('citizenship', 'India')}
Institution: {academic.get('current_institution', 'Christ University')}
Degree: {academic.get('degree', 'B.Tech')} ({academic.get('degree_level', 'Undergraduate')})
Major: {academic.get('major', 'Computer Science and Engineering')}
Current Year: {academic.get('current_year', 'Third Year')}
GPA: {gpa} / {gpa_scale}
Household Income: {income_str}
Financial Need Demonstrated: {'Yes' if financial.get('financial_need_demonstrated') else 'No'}
""".strip()