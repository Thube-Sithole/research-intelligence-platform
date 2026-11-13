from app.graph.state import ResearchState


def plan_research(state: ResearchState) -> ResearchState:
    """Create a transparent starter plan for researcher review."""

    question = state["question"]

    research_plan = [
        f"Clarify the key concepts and operational definitions in: {question}",
        "Identify relevant disciplines, variables, populations or system boundaries.",
        "Define source inclusion, exclusion and date criteria with the researcher.",
        "Retrieve sources and record exactly what content was accessible.",
        "Extract findings, assess quality, compare evidence and identify gaps.",
    ]

    return {
        "research_plan": research_plan,
        "status": "plan_ready_for_review",
        "workflow_events": [
            {
                "event": "plan_created",
                "actor": "system",
                "run_id": state.get("run_id"),
                "status": "plan_ready_for_review",
            }
        ],
    }