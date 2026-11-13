from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_research_run_is_transparent_about_scaffold():
    response = client.post(
        "/api/v1/research/runs",
        json={
            "question": "How does reflux ratio influence distillation column performance?",
            "domain": "engineering",
            "project_id": "demo-project",
            "memory_scope": "project",
            "autonomy": "hybrid",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "awaiting_source_integration"
    assert body["sources"] == []
    assert "no sources were retrieved" in body["notice"]
