import os
import json
import asyncio
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.services.mock_portal import router as mock_portal_router
from backend.services.profile_service import ProfileService
from backend.agents.orchestrator import OrchestratorAgent

app = FastAPI(
    title="Application Readiness Agent",
    description="Browser agent helping candidates prepare applications for scholarships, internships, and university programs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mock_portal_router)

orchestrator = OrchestratorAgent()
profile_service = ProfileService()

class WorkflowRequest(BaseModel):
    url: str
    program_name: Optional[str] = ""

class ProfileUpdateRequest(BaseModel):
    profile_data: Dict[str, Any]

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Application Readiness Agent",
        "webcmd_version": "0.7.4",
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY"))
    }

@app.get("/api/profile")
async def get_profile():
    return profile_service.get_profile()

@app.put("/api/profile")
async def update_profile(req: ProfileUpdateRequest):
    success = profile_service.save_profile(req.profile_data)
    return {"ok": success}

@app.get("/api/documents")
async def get_documents():
    return orchestrator.document_agent.get_local_documents()

@app.post("/api/workflow/start")
async def start_workflow(req: WorkflowRequest):
    async def event_generator():
        async for state_update in orchestrator.execute_workflow(req.url, req.program_name):
            yield f"data: {json.dumps(state_update)}\n\n"
            await asyncio.sleep(0.05)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/api/workflow/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    return orchestrator.get_workflow(workflow_id)

@app.post("/api/workflow/approve/{workflow_id}")
async def approve_workflow(workflow_id: str):
    return orchestrator.approve_workflow(workflow_id)

@app.get("/api/presets")
async def get_presets():
    return [
        {
            "id": "stem_scholarship_2026",
            "name": "Global NextGen STEM Scholars Program 2026",
            "organization": "Future Innovators Foundation",
            "url": "http://localhost:8000/demo-portal",
            "type": "Scholarship ($15,000 USD)",
            "deadline": "Oct 15, 2026",
            "badge": "Built-in Live Demo"
        },
        {
            "id": "ai_fellowship_2026",
            "name": "AI & Society Graduate Research Fellowship",
            "organization": "Center for Responsible Intelligence",
            "url": "http://localhost:8000/demo-portal",
            "type": "Fellowship ($25,000 USD)",
            "deadline": "Nov 30, 2026",
            "badge": "Built-in Live Demo"
        },
        {
            "id": "open_source_internship",
            "name": "Global Open Source Software Internship",
            "organization": "Open Source Tech Alliance",
            "url": "http://localhost:8000/demo-portal",
            "type": "Paid Internship ($8,000 / month)",
            "deadline": "Dec 01, 2026",
            "badge": "Built-in Live Demo"
        }
    ]