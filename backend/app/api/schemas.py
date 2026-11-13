
from typing import Literal

from pydantic import BaseModel, Field


class ResearchRunRequest(BaseModel):
    question: str = Field(
        min_length=12,
        max_length=4000
    )

    domain: str = Field(
        default="general",
        min_length=2,
        max_length=80
    )

    project_id: str = Field(
        min_length=1,
        max_length=120
    )

    memory_scope: Literal[
        "project",
        "shared",
        "both"
    ] = "both"

    autonomy: Literal["hybrid"] = "hybrid"


class ResearchRunResponse(BaseModel):
    run_id: str
    project_id: str
    status: str
    research_plan: list[str]
    sources: list[dict]
    notice: str
