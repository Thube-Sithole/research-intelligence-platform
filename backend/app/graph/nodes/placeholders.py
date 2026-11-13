from app.graph.state import ResearchState


def mark_discovery_pending(state: ResearchState) -> ResearchState:
    """Mark literature discovery as pending until providers are integrated."""

    return {
        "sources": [],
        "status": "awaiting_source_integration",
        "workflow_events": [
            {
                "event": "literature_discovery_not_configured",
                "actor": "system",
                "run_id": state.get("run_id"),
                "memory_scope": state.get("memory_scope"),
            }
        ],
    }