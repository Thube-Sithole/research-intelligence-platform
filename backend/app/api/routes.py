from uuid import uuid4
from fastapi import APIRouter

from app.api.schemas import ResearchRunRequest, ResearchRunResponse
from app.graph.workflow import research_graph

router = APIRouter()


@router.post("/research/runs", response_model=ResearchRunResponse)
async def create_research_run(payload: ResearchRunRequest):
    run_id = str(uuid4())
    initial_state = {
        "run_id": run_id,
        "project_id": payload.project_id,
        "question": payload.question,
        "domain": payload.domain,
        "memory_scope": payload.memory_scope,
        "autonomy": payload.autonomy,
        "workflow_events": [],
    }
    result = await research_graph.ainvoke(initial_state)
    return ResearchRunResponse(
        run_id=run_id,
        project_id=payload.project_id,
        status=result.get("status", "unknown"),
        research_plan=result.get("research_plan", []),
        sources=result.get("sources", []),
        notice=("Starter scaffold only: no literature providers are connected, so no sources "
                "were retrieved and no research conclusions have been generated."),
    )
