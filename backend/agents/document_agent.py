import os
import json
import logging
from typing import Dict, Any, List
from ..services.llm_service import LLMService

logger = logging.getLogger("agents.document")

class DocumentAgent:
    def __init__(self, llm: LLMService, docs_dir: str = None):
        self.llm = llm
        if docs_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.docs_dir = os.path.join(base_dir, "demo_data", "documents")
        else:
            self.docs_dir = docs_dir

    def get_local_documents(self) -> List[Dict[str, Any]]:
        index_file = os.path.join(self.docs_dir, "demo_documents_index.json")
        if os.path.exists(index_file):
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading doc index: {e}")
        
        docs = []
        if os.path.exists(self.docs_dir):
            for fname in os.listdir(self.docs_dir):
                if fname.endswith((".pdf", ".txt", ".docx", ".png", ".jpg")):
                    docs.append({
                        "id": fname,
                        "filename": fname,
                        "title": fname.replace("_", " ").title(),
                        "category": "general",
                        "tags": [fname.split(".")[0]],
                        "sample": True
                    })
        return docs

    async def verify_documents(self, required_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cross-references required application documents against candidate's vault.
        """
        logger.info(f"DocumentAgent verifying {len(required_documents)} required documents")
        local_docs = self.get_local_documents()
        result = self.llm.match_documents(required_documents, local_docs)
        result["available_vault_documents"] = local_docs
        return result