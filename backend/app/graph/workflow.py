from langgraph.graph import END, START, StateGraph

from app.graph.nodes.planner import plan_research
from app.graph.nodes.placeholders import mark_discovery_pending
from app.graph.state import ResearchState


def build_research_graph():
    """Build the first safe workflow slice. Persistent checkpoints come in a later milestone."""
    graph = StateGraph(ResearchState)
    graph.add_node("planner", plan_research)
    graph.add_node("discovery_placeholder", mark_discovery_pending)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "discovery_placeholder")
    graph.add_edge("discovery_placeholder", END)
    return graph.compile()


research_graph = build_research_graph()
