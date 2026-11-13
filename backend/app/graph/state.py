
from typing import Annotated, Literal, TypedDict
import operator


MemoryScope = Literal["project", "shared", "both"]
AutonomyMode = Literal["hybrid"]


class ResearchState(TypedDict, total=False):
    # Research identity
    run_id: str
    project_id: str

    # Research configuration
    question: str
    domain: str
    memory_scope: MemoryScope
    autonomy: AutonomyMode

    # Research planning
    research_plan: list[str]

    # Evidence discovery and extraction
    sources: list[dict]
    evidence_items: list[dict]

    # Research intelligence
    analysis: dict
    critique: dict
    synthesis: dict

    # Workflow management
    status: str
    workflow_events: Annotated[list[dict], operator.add]
    errors: list[str]
